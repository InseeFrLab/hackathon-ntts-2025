import os
import glob
import rasterio
import numpy as np
import geopandas as gpd
import folium
from rasterio.features import shapes
from shapely.geometry import shape, MultiPolygon
from src.export_clc_plus_labels import download_label
import s3fs
import pandas as pd

from astrovision.data.satellite_image import (
    SatelliteImage,
)

fs = s3fs.S3FileSystem(
    client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
    key = os.environ["AWS_ACCESS_KEY_ID"], 
    secret = os.environ["AWS_SECRET_ACCESS_KEY"]
    )
# --- Étape 1 : Définition des fichiers pour 2018 et 2021 ---

picture_dir = "projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/"
label_dir = "projet-hackathon-ntts-2025/data-preprocessed/labels/CLCplus-Backbone/SENTINEL2/"

NUTS3S = ["BE100","BE251","FRJ27","FRK26"]
NUTS3S=["BG322","CY000","CZ072","DEA54","DK041","EE00A","EL521","ES612","FI1C1","BE100","BE251","FRJ27","FRK26"]
years=["2018","2021"]
results=[]

for NUTS3 in NUTS3S:
    print(NUTS3)
    for year in years :
        # year, NUTS3 = ["2018","BE100"]
        label_dir= f"data-preprocessed/labels/CLCplus-Backbone/SENTINEL2/{NUTS3}/{year}/250/"
        os.makedirs(label_dir,exist_ok = True)
        export_url = f"https://copernicus.discomap.eea.europa.eu/arcgis/rest/services/CLC_plus/CLMS_CLCplus_RASTER_{year}_010m_eu/ImageServer/exportImage"
        path_parquet = f"s3://projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/{NUTS3}/{year}/250/filename2bbox.parquet"

        with fs.open(path_parquet,"rb") as filename:
            filename2bbox = pd.read_parquet(filename)

#        row = filename2bbox.iloc[0]
        for index, row in filename2bbox.iterrows():
            bbox_tuple = tuple(map(int, row.bbox))
            filename = row.filename

            xmin, ymin, xmax, ymax = bbox_tuple

            resolution = 10

            # Calcul de la taille en pixels pour garantir 1 pixel = 10 m
            size_x = int((xmax - xmin) / resolution)
            size_y = int((ymax - ymin) / resolution)

            # Construction de la bounding box sous forme de chaîne
            bbox_str = f"{xmin},{ymin},{xmax},{ymax}"

            # Paramètres communs pour l'export
            common_params = {
                "f": "image",
                "bbox": bbox_str,
                "bboxSR": "3035",   # Lambert-93
                "imageSR": "3035",  # Sortie aussi en Lambert-93
                "size": f"{size_x},{size_y}",  # Ajusté automatiquement pour 1 pixel = 10 m
            }

            download_label("tiff", label_dir+filename, common_params, export_url)

gdf_list=[]
NUTS3S=["BG322","CY000","CZ072","DEA54","DK041","EE00A","EL521","ES612","FI1C1","BE100","BE251","FRJ27","FRK26"]

for NUTS3 in NUTS3S :
    print(NUtS3)
    label_dir= f"data-preprocessed/labels/CLCplus-Backbone/SENTINEL2/{NUTS3}"
    # Lister les fichiers .tif pour 2018 et 2021
    tif_2018_files = sorted(glob.glob(os.path.join(label_dir, "2018/250/*.tif")))
    tif_2021_files = sorted(glob.glob(os.path.join(label_dir, "2021/250/*.tif")))

    # Vérification que les listes de fichiers sont cohérentes
    assert len(tif_2018_files) == len(tif_2021_files), "Nombre de fichiers différent entre 2018 et 2021 !"
    
    # --- Étape 2 : Fonction pour binariser un raster (Classe 1 → 1, autres → 0) ---
    def load_and_binarize_raster(path):
        """Charge un raster et binarise : classe 1 → 1, autres → 0"""
        with rasterio.open(path) as src:
            image = src.read(1)  # Lire la première bande
            transform = src.transform  # Transformation géospatiale
        binary_image = np.where(image == 1, 1, 0).astype(np.uint8)
        return binary_image, transform


    # --- Étape 3 : Calculer la différence des rasters et extraire les polygones ---
    features = []

    for tif_2018, tif_2021 in zip(tif_2018_files, tif_2021_files):
        # Charger les rasters binarisés
        binary_2018, transform = load_and_binarize_raster(tif_2018)
        binary_2021, _ = load_and_binarize_raster(tif_2021)

        # Matrice de changement des classes
        change_matrix = binary_2018 * 2 + binary_2021  # (00 → 0, 01 → 1, 10 → 2, 11 → 3)

        # Extraction des polygones uniquement pour les zones ayant changé (≠ 0)
        for shape_dict, value in shapes(change_matrix, transform=transform):
            if value > 0:  # Exclure les zones sans changement
                features.append({"geometry": shape(shape_dict), "class": int(value)})

    # --- Étape 4 : Convertir en GeoDataFrame ---
    SRC_CRS = "EPSG:3035"  # Lambert-93
    TARGET_CRS = "EPSG:4326"  # WGS 84 (GPS)

    gdf = gpd.GeoDataFrame(features, crs=SRC_CRS).to_crs(TARGET_CRS)
    print(gdf)
    gdf_list.append(gdf)



# Concatenate all GeoDataFrames
gdf_concatenated = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))


# Sauvegarde en shapefile (optionnel)
gdf_concatenated.to_file(f"change_polygons_CLC.gpkg")
lpath =f"change_polygons_CLC.gpkg"
rpath =f"s3://projet-hackathon-ntts-2025/indicators/"

fs.put(lpath,rpath)
