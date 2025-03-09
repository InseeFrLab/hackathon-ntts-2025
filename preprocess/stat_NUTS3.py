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

NUTS3S = ["BG322", "CY000", "CZ072", "DEA54", "EE00A", "EL521", "ES612", "FI1C1", "BE100", "BE251", "FRJ27", "FRK26","UKJ22"]
NUTS3S=["UKJ22"]
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
    bati_2021 = 0

    import numpy as np

    # Boucle sur plusieurs départements
    for i in range(len(list_labels_2018)):
        # Charger les labels bâti
        with fs.open(list_labels_2018[i], 'rb') as f:
            label_2018 = np.load(f)

        with fs.open(list_labels_2021[i], 'rb') as f:
            label_2021 = np.load(f)

        sat18 = SatelliteImage.from_raster(
            file_path=f"/vsis3/{list_patchs_2018[i]}",
            n_bands=14,
        )

        sat21 = SatelliteImage.from_raster(
            file_path=f"/vsis3/{list_patchs_2021[i]}",
            n_bands=14,
        )

        # Charger les NDVI
        ndvi_2018 = sat18.array[12]
        ndvi_2021 = sat21.array[12]

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
        bati_2021 += np.sum(label_2021 == 1)
        

    # Ajouter les résultats à la liste
    results.append({
        "NUTS3": NUTS3,
        "NDVI+": ajout_ndvi,
        "NDVI-": suppression_ndvi,
        "artificial+": ajout_bati,
        "artificial-": suppression_bati,
        "artificial_2021": bati_2021
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
df_results = df_results[["NUTS3", "artificial_2021",
                         "artificial+", "artificial-", "artificial_net",
                         "NDVI+", "NDVI-", "NDVI_net"]]



fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": f"https://{os.environ['AWS_S3_ENDPOINT']}"},
    key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# Remplacez par le chemin exact vers votre fichier .gpkg sur S3
gpkg_s3_path = "projet-hackathon-ntts-2025/NUTS_RG_01M_2021_4326_LEVL_3.gpkg"

# Téléchargement local du GeoPackage depuis S3
local_gpkg = "/tmp/NUTS_RG_01M_2021_4326_LEVL_3.gpkg"
with fs.open(gpkg_s3_path, "rb") as remote_file:
    with open(local_gpkg, "wb") as f:
        f.write(remote_file.read())

gdf = gpd.read_file(local_gpkg)

# Filtrer les NUTS_ID présents dans df_results
nuts_ids = df_results["NUTS3"].tolist()
gdf_filtered = gdf[gdf["NUTS_ID"].isin(nuts_ids)].copy()

gdf_filtered = gdf_filtered.to_crs(epsg=3035)

# Calculer la surface en m²
gdf_filtered["surface_m2"] = gdf_filtered.geometry.area
gdf_filtered = gdf_filtered[["NUTS_ID","surface_m2"]]
# Fusionner avec df_results pour récupérer les valeurs d'artificialisation

df_results = df_results.merge(gdf_filtered, left_on="NUTS3", right_on="NUTS_ID", how="left")
df_results["artificial_ratio"] = (100*(df_results["artificial_2021"]/df_results["surface_m2"])).round(2)
# Save DataFrame as a Parquet file
df_results.to_parquet("indicateurs_departements.parquet", engine="pyarrow", index=False)

lpath =f"indicateurs_departements.parquet"
rpath =f"s3://projet-hackathon-ntts-2025/indicators/"

fs.put(lpath,rpath)


# test
import os
import s3fs
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": f"https://{os.environ['AWS_S3_ENDPOINT']}"},
    key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# Remplacez par le chemin exact vers votre fichier .gpkg sur S3
gpkg_s3_path = "projet-hackathon-ntts-2025/data-predictions/CLCplus-Backbone/SENTINEL2/2024/250/predictions_FRK26.gpkg"

# Téléchargement local du GeoPackage depuis S3
local_gpkg = "/tmp/predictions_FRK26.gpkg"
with fs.open(gpkg_s3_path, "rb") as remote_file:
    with open(local_gpkg, "wb") as f:
        f.write(remote_file.read())

