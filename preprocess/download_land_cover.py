import requests
from PIL import Image
import pandas as pd
import numpy as np
import os
import s3fs
# URL exportImage du service Copernicus


fs = s3fs.S3FileSystem(
    client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
    key = os.environ["AWS_ACCESS_KEY_ID"], 
    secret = os.environ["AWS_SECRET_ACCESS_KEY"]
    )

# Define S3 File Path
s3_path_s2  = "s3://projet-hackathon-ntts-2025/data-raw/SENTINEL2"
NUTS3 = "FRJ27" 
year = "2018"
parquet_name = "filename2bbox.parquet"

# Construct the S3 path dynamically
s3_path = f"{s3_path_s2}/{NUTS3}/{year}/{parquet_name}"

os.makedirs(f"{"labels"}/{NUTS3}/{year}")

# export_url = (
#     "https://copernicus.discomap.eea.europa.eu/"
#     "arcgis/rest/services/CLC_plus/CLMS_CLCplus_RASTER_2021_010m_eu/"
#     "ImageServer/exportImage"
# )

export_url = f"https://copernicus.discomap.eea.europa.eu/arcgis/rest/services/CLC_plus/CLMS_CLCplus_RASTER_{year}_010m_eu/ImageServer/exportImage"

# Configure S3 Filesystem for MinIO
fs = s3fs.S3FileSystem(
    client_kwargs={'endpoint_url': 'https://' + 'minio.lab.sspcloud.fr'},
    key=os.environ["AWS_ACCESS_KEY_ID"], 
    secret=os.environ["AWS_SECRET_ACCESS_KEY"]
)

with fs.open(s3_path, "rb") as f:
    df = pd.read_parquet(f)

def download_image(format_ext, filename, common_params, export_url):
    """Télécharge une image dans le format spécifié (tiff ou png)"""
    params = common_params.copy()
    params["format"] = format_ext

    response = requests.get(export_url, params=params, stream=True)

    if response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"):
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        #print(f"Téléchargement {format_ext.upper()} terminé : {filename}")
    else:
        print(f"Erreur {format_ext.upper()} : ", response.status_code, response.text)

#row = df.iloc[0]
#row.bbox
for index, row in df.iterrows():
    
    bbox_tuple = tuple(map(int, row.bbox))  # Convertir bbox en tuple d'entiers
    filename = row.filename  # Récupérer le nom du fichier
    
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
    # Construct the S3 path dynamically
    l_path = f"{"labels"}/{NUTS3}/{year}/"

    download_image("tiff",l_path+filename, common_params,export_url)
    
    img = Image.open(l_path+filename)
    npy_filename = filename.replace(".tif", ".npy")
    np.save(l_path + npy_filename,np.array(img))

    if os.path.exists(l_path+filename):
        os.remove(l_path+filename)

    fs.put(
        l_path+npy_filename,
        f"{"s3://projet-hackathon-ntts-2025/data-label/CLCplus-Backbone"}/{NUTS3}/{year}/",
        True
    )



import numpy as np
from PIL import Image

npy_filename ="3924340_3097760_0_60.npy"

# Charger le fichier .npy
img_array = np.load(l_path + npy_filename)
projet-hackathon-ntts-2025/data-label/CLCplus-Backbone
# Créer une image binaire : Classe 1 → Blanc (255), Autres → Noir (0)
binary_img = np.where(img_array == 1, 255, 0).astype(np.uint8)

# Convertir en image et sauvegarder en PNG
output_png = "output_class1.png"
Image.fromarray(binary_img).save(output_png)

print(f"Image sauvegardée sous : {output_png}")

