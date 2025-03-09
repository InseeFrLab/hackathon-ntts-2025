import os
import tempfile

import geopandas as gpd
import pandas as pd
import s3fs


def get_system_file():
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": "https://" + "minio.lab.sspcloud.fr"},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
    return fs


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


def concatenate_gpkg(year: int):
    fs = get_system_file()
    s3_dir = (
        f"s3://projet-hackathon-ntts-2025/data-predictions/CLCplus-Backbone/SENTINEL2/{year}/250/"
    )
    gpkg_filepaths = [fp for fp in fs.ls(s3_dir) if fp.endswith(".gpkg")]

    gdf_list = []
    for filepath in gpkg_filepaths:
        with fs.open(filepath, "rb") as f:
            mini_gdf = gpd.read_file(f, driver="GPKG")
        gdf_list.append(mini_gdf)

    gdf = pd.concat(gdf_list, ignore_index=True)

    save_geopackage_to_s3(gdf, s3_dir + "predictions_UE.gpkg", fs)
