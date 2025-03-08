import requests
import s3fs
import os
import json
import geopandas as gpd
import argparse
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster tiling pipeline")
    parser.add_argument("--nuts3", type=str, required=True, help="NUTS3 (e.g., 'BE100')")
    parser.add_argument("--year", type=int, required=True, help="startDate (e.g., 2024)")
    args = parser.parse_args()

    nuts3 = args.nuts3
    year = args.year

    start_time = time.time()

    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
        key=os.environ["AWS_ACCESS_KEY_ID"], 
        secret=os.environ["AWS_SECRET_ACCESS_KEY"]
        )

    url = "https://hackathon-ntts-2025.lab.sspcloud.fr/predict_nuts"
    response = requests.get(url, params={'nuts_id': nuts3, 'year': year})

    geojson_string = response.json()["predictions"]
    geojson_obj = json.loads(geojson_string)

    data = []
    for feature in geojson_obj["features"]:
        feature_id = feature["id"]
        label = feature["properties"]["label"]
        coordinates = feature["geometry"]["coordinates"]

        data.append({"id": feature_id, "label": label, "coordinates": coordinates})
    df = gpd.GeoDataFrame(data)

    filepath_out = f"s3://projet-hackathon-ntts-2025/data-predictions/CLCplus-Backbone/SENTINEL2/{year}/250/"
    with fs.open(filepath_out, 'wb') as f:
        df.to_file(f, driver="GPKG", index=False)

    end_time = time.time() - start_time
    print(f"{nuts3} predicted in {round(end_time/60)} min and registered here {filepath_out}")
