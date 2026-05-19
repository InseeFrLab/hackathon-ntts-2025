"""
Main file for the API.
"""

import gc
import os
from contextlib import asynccontextmanager
from typing import Dict, List, Annotated, Optional

import geopandas as gpd
import mlflow
import numpy as np
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from osgeo import gdal

from app.logger_config import configure_logger
from app.utils import (
    create_geojson_from_mask,
    get_cache_path,
    get_file_system,
    get_model,
    get_normalization_metrics,
    load_from_cache,
    predict,
    produce_mask,
    find_nuts3_of_gps_point,
    find_gps_point_in_filename2bbox
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for managing the lifespan of the API.
    This context manager is used to load the ML model and other resources
    when the API starts and clean them up when the API stops.
    Args:
        app (FastAPI): The FastAPI application.
    """
    global \
        logger, \
        model, \
        n_bands, \
        tiles_size, \
        augment_size, \
        module_name, \
        normalization_mean, \
        normalization_std

    gdal.UseExceptions()
    logger = configure_logger()

    model_name: str = os.getenv("MLFLOW_MODEL_NAME")
    model_version: str = os.getenv("MLFLOW_MODEL_VERSION")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI")

    # Load the ML model
    model = get_model(model_name, model_version, mlflow_tracking_uri)

    # Extract several variables from model metadata
    n_bands = int(mlflow.get_run(model.metadata.run_id).data.params["n_bands"])
    tiles_size = int(mlflow.get_run(model.metadata.run_id).data.params["tiles_size"])
    augment_size = int(mlflow.get_run(model.metadata.run_id).data.params["augment_size"])
    module_name = mlflow.get_run(model.metadata.run_id).data.params["module_name"]
    normalization_mean, normalization_std = get_normalization_metrics(model, n_bands)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Satellite Image Inference",
    description="Segment satellite images",
    version="0.0.1",
)


@app.get("/", tags=["Welcome"])
def show_welcome_page():
    """
    Show welcome page with current model name and version.
    """
    model_name: str = os.getenv("MLFLOW_MODEL_NAME")
    model_version: str = os.getenv("MLFLOW_MODEL_VERSION")
    return {
        "message": "Satellite Image Inference",
        "model_name": f"{model_name}",
        "model_version": f"{model_version}",
    }


@app.get("/find_nuts", tags=["Find NUTS3"])
async def find_nuts(
    gps_point: Annotated[List[float], Query(
        min_length=2,
        max_length=2,
        description="[latitude, longitude] in WGS84",
        example=[49.633339659666575, 6.168944599158566]
    )],
) -> str:
    """
    Find NUTS3 id for a given gps point.

    Args:
        gps_point (List[float]): [latitude, longitude] of the GPS point in WGS84.
    Returns:
        str: NUTS3 id if found, otherwise empty string.
    """
    gc.collect()
    logger.info(f"Find the image filepath for this gps point: {gps_point}")

    nuts_id = find_nuts3_of_gps_point(gps_point)

    if nuts_id:
        logger.info(f"GPS point found in NUTS3='{nuts_id}'")
        return nuts_id

    logger.warning("GPS point not found in any NUTS3")
    return ""


@app.get("/find_image", tags=["Find Image"])
async def find_image(
    gps_point: Annotated[List[float], Query(
        min_length=2,
        max_length=2,
        description="[latitude, longitude] in WGS84",
        example=[49.633339659666575, 6.168944599158566]
    )],
    year: int = Query(..., ge=2018, le=2024, example=2021),
    nuts_id: Optional[str] = Query(None, example="LU000")
) -> str:
    """
    Find image path for a given gps point, year and potentielly NUTS3 id.

    Args:
        gps_point (List[float]): [latitude, longitude] of the GPS point in WGS84.
        year (int): The year of the satellite images.
        Optional - nuts_id (str): The ID of the NUTS.
    Returns:
        str: Image filepath if found, otherwise empty string.
    """
    gc.collect()
    logger.info(f"Find the image filepath for this gps point: {gps_point}")

    base_path = "projet-funathon/2026/project3/data/images"
    image_filename = ""

    if not nuts_id:
        nuts_id = find_nuts3_of_gps_point(gps_point)

    if nuts_id:
        url = f"https://minio.lab.sspcloud.fr/{base_path}/{nuts_id}/{year}/filename2bbox.parquet"

        try:
            df = pd.read_parquet(url)
            image_filename = find_gps_point_in_filename2bbox(df, gps_point)
            if image_filename:
                image_filepath = f"{base_path}/{nuts_id}/{year}/{image_filename}"
                logger.info(f"GPS point found in NUTS3='{nuts_id}' year={year}")
                return image_filepath
            else:
                logger.warning(f"GPS point not found in NUTS3='{nuts_id}' year={year}")
                return ""

        except Exception:
            logger.warning(f"No data for NUTS3='{nuts_id}' and year={year}")
            return ""

    logger.warning(f"GPS point not found in any NUTS3 for year={year}")
    return ""


@app.get("/predict_image", tags=["Predict Image"])
async def predict_image(
    image: str = Query(
        ...,
        example="projet-funathon/2026/project3/data/images/LU000/2021/4042000_2951690_0_637.tif"
    ),
    polygons: bool = Query(False, description="Return polygons instead of raster mask")
) -> Dict:
    """
    Predicts mask for a given satellite image.

    Args:
        image (str): Path to the satellite image.
        polygons (bool, optional): Flag indicating whether to include polygons in the response.
        Defaults to False.

    Returns:
        Dict: Response containing the mask of the prediction.

    Raises:
        ValueError: If the dimension of the image is not divisible by the tile size used during
        training or if the dimension is smaller than the tile size.

    """
    logger.info(f"Predict image endpoint accessed with image: {image}")
    gc.collect()

    fs = get_file_system()

    if not fs.exists(get_cache_path(image)):
        lsi = predict(
            images=image,
            model=model,
            tiles_size=tiles_size,
            augment_size=augment_size,
            n_bands=n_bands,
            normalization_mean=normalization_mean,
            normalization_std=normalization_std,
            module_name=module_name,
        )
        # Save predictions to cache
        with fs.open(get_cache_path(image), "wb") as f:
            np.save(f, lsi.label)

    else:
        logger.info(f"Loading prediction from cache for image: {image}")
        lsi = load_from_cache(image, n_bands, fs)

    # Produce mask with class IDs
    lsi.label = produce_mask(lsi.label, module_name)

    if polygons:
        return JSONResponse(content=create_geojson_from_mask(lsi).to_json())
    else:
        return {"mask": lsi.label.tolist()}


@app.get("/predict_nuts", tags=["Predict NUTS"])
def predict_nuts(
    nuts_id: str = Query(..., example="LU000"),
    year: int = Query(..., ge=2018, le=2024),
) -> Dict:
    """
    Predicts nuts for a given NUTS ID, year, and department.

    Args:
        nuts_id (str): The ID of the NUTS.
        year (int): The year of the satellite images.
    Returns:
        Dict: Response containing the predicted NUTS.
    """
    logger.info(f"Predict nuts endpoint accessed with nuts_id: {nuts_id}, year: {year}")

    fs = get_file_system()

    # # Get NUTS file
    # nuts = gpd.read_file("/api/nuts_2021.gpkg")
    # nuts = gpd.GeoDataFrame(nuts, geometry="geometry", crs="EPSG:4326")

    path = f"s3://projet-funathon/2026/project3/data/images/{nuts_id}"

    if fs.exists(path):
        logger.info(f"{nuts_id} is in the database")
    else:
        logger.info(f"""No {nuts_id} in the database.""")
        return JSONResponse(
            content={
                "predictions": gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:3035").to_json()
            }
        )

    if fs.exists(path+f"/{year}"):
        logger.info(f"{year} is in the database for {nuts_id}.")
    else:
        logger.info(f"""No {year} in {nuts_id} in the database.""")
        return JSONResponse(
            content={
                "predictions": gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:3035").to_json()
            }
        )

    images = [
        img
        for img in fs.ls(
            path+f"/{year}/"
        )
        if img.endswith(".tif")
    ]

    # Check if images are found in S3 bucket
    if not images:
        logger.info(f"""No images found for nuts_id: {nuts_id} and year: {year}""")
        return JSONResponse(
            content={
                "predictions": gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:3035").to_json()
            }
        )

    images_to_predict = [im for im in images if not fs.exists(get_cache_path(im))]
    images_from_cache = [im for im in images if fs.exists(get_cache_path(im))]
    predictions = []

    if images_to_predict:
        # Predict
        predictions = predict(
            images_to_predict,
            model,
            tiles_size,
            augment_size,
            n_bands,
            normalization_mean,
            normalization_std,
            module_name,
        )

        # Save predictions to cache
        for im, pred in zip(images_to_predict, predictions):
            with fs.open(get_cache_path(im), "wb") as f:
                np.save(f, pred.label)

    if images_from_cache:
        logger.info(
            f"""Loading predictions from cache for images: {", ".join(images_from_cache)}"""
        )
        # Load from cache
        predictions += [load_from_cache(im, n_bands, fs) for im in images_from_cache]

    # Produce mask with class IDs TODO : check if ok
    for lsi in predictions:
        lsi.label = produce_mask(lsi.label, module_name)

    preds = pd.concat([create_geojson_from_mask(x) for x in predictions])

    response_data = {
        "predictions": preds.to_json(),
    }

    return JSONResponse(content=response_data)
