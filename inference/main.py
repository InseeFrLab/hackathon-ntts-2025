import argparse
import json
import os
import tempfile
import time

import geopandas as gpd
import requests
import s3fs
from shapely.geometry import shape


def save_geopackage_to_s3(gdf, s3_path, filesystem):
    """
    Save a GeoDataFrame as a GeoPackage to S3.

    Parameters:
    -----------
    gdf : geopandas.GeoDataFrame
        The GeoDataFrame to save
    s3_path : str
        The S3 path where to save the file (including .gpkg extension)
    filesystem : s3fs.S3FileSystem
        Initialized S3 filesystem object
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".gpkg", delete=False) as tmp_file:
        temp_path = tmp_file.name

    try:
        # Save to temporary file
        gdf.to_file(temp_path, driver="GPKG")

        # Upload to S3
        with open(temp_path, "rb") as file:
            with filesystem.open(s3_path, "wb") as s3_file:
                s3_file.write(file.read())
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster tiling pipeline")
    parser.add_argument("--nuts3", type=str, required=True, help="NUTS3 (e.g., 'BE100')")
    parser.add_argument("--year", type=int, required=True, help="startDate (e.g., 2024)")
    args = parser.parse_args()

    nuts3 = args.nuts3
    year = args.year

    start_time = time.time()

    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": "https://" + "minio.lab.sspcloud.fr"},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
    print(f"Start of the prediction of NUTS {nuts3}")
    # nuts3="BE100"
    # year="2024"
    url = "https://hackathon-ntts-2025.lab.sspcloud.fr/predict_nuts"
    response = requests.get(url, params={"nuts_id": nuts3, "year": year})

    if response.status_code == 200:
        print("Prediction done, now register on s3")
        geojson_string = response.json()["predictions"]
        geojson_obj = json.loads(geojson_string)

        data = []
        for feature in geojson_obj["features"]:
            feature_id = feature["id"]
            label = feature["properties"]["label"]
            coordinates = feature["geometry"]["coordinates"]

            data.append({"id": feature_id, "label": label, "coordinates": coordinates})

        df = gpd.GeoDataFrame(data)

        df["geometry"] = df["coordinates"].apply(
            lambda x: shape({"type": "Polygon", "coordinates": x})
        )
        gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:3035")

        gdf = gdf.drop(columns=["coordinates", "id"])

        filepath_out = f"s3://projet-hackathon-ntts-2025/data-predictions/CLCplus-Backbone/SENTINEL2/{year}/250/predictions_{nuts3}.gpkg"
        save_geopackage_to_s3(df, filepath_out, fs)

        end_time = time.time() - start_time
        print(f"{nuts3} predicted in {round(end_time/60)} min and registered here {filepath_out}")
    else:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")
