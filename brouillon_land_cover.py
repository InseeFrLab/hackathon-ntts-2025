import requests

# URL exportImage du service Copernicus
export_url = (
    "https://copernicus.discomap.eea.europa.eu/"
    "arcgis/rest/services/CLC_plus/CLMS_CLCplus_RASTER_2021_010m_eu/"
    "ImageServer/exportImage"
)


# Bounding box (Lambert-93, EPSG:2154) : 2,5 km × 2,5 km autour de Paris
xmin, ymin, xmax, ymax = (647592, 6858866, 650092, 6861366)

# Calcul du facteur d'élargissement (x5)
expand_factor = 5
width = xmax - xmin  # 2500 m
height = ymax - ymin  # 2500 m

new_width = width * expand_factor
new_height = height * expand_factor

# Ajustement des coordonnées pour élargir symétriquement
xmin -= new_width // 2
xmax += new_width // 2
ymin -= new_height // 2
ymax += new_height // 2

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
    "bboxSR": "2154",   # Lambert-93
    "imageSR": "2154",  # Sortie aussi en Lambert-93
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
download_image("tiff", "clcplus2021_paris_10m.tif")
download_image("png", "clcplus2021_paris_10m.png")

try:
    img = Image.open("clcplus2021_paris_10m.tif")
    img.show()
    print("TIFF ouvert avec succès.")
except Exception as e:
    print("Erreur à l'ouverture du TIFF :", e)

np.array(img)
np.unique(img) = 10