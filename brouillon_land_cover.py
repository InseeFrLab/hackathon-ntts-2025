import requests

# URL exportImage du service Copernicus
export_url = (
    "https://copernicus.discomap.eea.europa.eu/"
    "arcgis/rest/services/CLC_plus/CLMS_CLCplus_RASTER_2018_010m_eu/"
    "ImageServer/exportImage"
)

from PIL import Image
import pandas as pd
import numpy as np

# Path to your local Parquet file
parquet_file = "hackathon-ntts-2025/filename2bbox.parquet"

# Lire le fichier Parquet
df = pd.read_parquet(parquet_file)

# Convertir la bounding box en tuple d'entiers
bbox_tuple = tuple(map(int, df.bbox[0]))
filename = df.filename

# Afficher le résultat
# Bounding box (Lambert-93, EPSG:2154) : 2,5 km × 2,5 km autour de Paris
xmin, ymin, xmax, ymax = (647592, 6858866, 650092, 6861366)
xmin, ymin, xmax, ymax = bbox_tuple

# Résolution cible en mètres par pixel
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

def download_image(format_ext, filename):
    """Télécharge une image dans le format spécifié (tiff ou png)"""
    params = common_params.copy()
    params["format"] = format_ext

    response = requests.get(export_url, params=params, stream=True)

    if response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"):
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Téléchargement {format_ext.upper()} terminé : {filename}")
    else:
        print(f"Erreur {format_ext.upper()} : ", response.status_code, response.text)

# --- Téléchargement des fichiers ---
download_image("tiff", "clcplus2016_test_10m.tif")
download_image("png", "clcplus2015_test_10m.png")

try:
    img = Image.open("clcplus2021_paris_10m.tif")
    img.show()
    print("TIFF ouvert avec succès.")
except Exception as e:
    print("Erreur à l'ouverture du TIFF :", e)


np.array(img)
np.unique(img)


# Afficher les 5 premières lignes
print(df.head())
