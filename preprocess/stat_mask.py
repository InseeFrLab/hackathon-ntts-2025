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

results=[]

for NUTS3 in NUTS3S:
    #NUTS3 = "BE100"
    print(NUTS3)

    list_labels_2018= fs.ls(f"{label_dir}{NUTS3}/{2018}/250")
    list_labels_2021= fs.ls(f"{label_dir}{NUTS3}/{2021}/250")
    list_patchs_2018 = fs.ls(f"{picture_dir}{NUTS3}/{2018}/250")
    list_patchs_2021 = fs.ls(f"{picture_dir}{NUTS3}/{2021}/250")

    # Initialiser les compteurs globaux
    total_ajout_ndvi = 0
    total_suppression_ndvi = 0
    total_ajout_bati = 0
    total_suppression_bati = 0

    # Boucle sur plusieurs départements
    for i in range(len(list_labels_2018)):
        # Charger les labels bâti
        with fs.open(list_labels_2018[i], 'rb') as f:
            label_2018 = np.load(f)

        with fs.open(list_labels_2021[i], 'rb') as f:
            label_2021 = np.load(f)

        # Charger les NDVI
        ndvi_2018 = SatelliteImage.from_raster(
            file_path=f"/vsis3/{list_patchs_2018[i]}",
            n_bands=14,
        ).array[12]

        ndvi_2021 = SatelliteImage.from_raster(
            file_path=f"/vsis3/{list_patchs_2021[i]}",
            n_bands=14,
        ).array[12]

        # Calcul des changements NDVI
        ajout_ndvi = np.sum((ndvi_2018 > 0.3) & (ndvi_2021 <= 0.3))  # Perte de végétation
        suppression_ndvi = np.sum((ndvi_2018 <= 0.3) & (ndvi_2021 > 0.3))  # Gain de végétation

        # Calcul des changements Bâti
        ajout_bati = np.sum((label_2018 != 1) & (label_2021 == 1))  # Ajout de bâti
        suppression_bati = np.sum((label_2018 == 1) & (label_2021 != 1))  # Suppression de bâti

        # Mise à jour des compteurs globaux
        total_ajout_ndvi += ajout_ndvi
        total_suppression_ndvi += suppression_ndvi
        total_ajout_bati += ajout_bati
        total_suppression_bati += suppression_bati

    # Ajouter les résultats à la liste
    results.append({
        "NUTS3": NUTS3,
        "NDVI+": ajout_ndvi,
        "NDVI-": suppression_ndvi,
        "artificial+": ajout_bati,
        "artificial-": suppression_bati
    })


# Convertir en DataFrame
df_results = pd.DataFrame(results)

pixel_to_m2 = 100
# Calcul de la différence nette en NDVI et artificialisation
df_results["NDVI_net"] = df_results["NDVI+"] - df_results["NDVI-"]
df_results["artificial_net"] = df_results["artificial+"] - df_results["artificial-"]


df_results["artificial+"] = df_results["artificial+"] * pixel_to_m2
df_results["artificial-"] = df_results["artificial-"] * pixel_to_m2
df_results["artificial_net"] = df_results["artificial_net"] * pixel_to_m2

# Conversion en m²
df_results["NDVI+"] = df_results["NDVI+"] * pixel_to_m2
df_results["NDVI-"] = df_results["NDVI-"] * pixel_to_m2
df_results["NDVI_net"] = df_results["NDVI_net"] * pixel_to_m2

# Réorganiser les colonnes
df_results = df_results[["NUTS3", 
                         "artificial+", "artificial-", "artificial_net",
                         "NDVI+", "NDVI-", "NDVI_net"]]

for NUTS3 in NUTS3S:
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
for NUTS3 in NUTS3S :
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
