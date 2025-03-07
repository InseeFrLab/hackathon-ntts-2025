import numpy as np
import os
from PIL import Image

# Définition des paramètres
file = "labels"
nuts3 = "FRK26"
years = [2018, 2021]
filename = "3879060_2555540_0_362.npy"

# Dictionnaire pour stocker les images binaires
masks = {}

# Fonction pour charger et traiter une année
def process_year(year):
    # Construire le chemin du fichier .npy
    npy_path = f"{file}/{nuts3}/{year}/{filename}"
    
    # Charger l'array numpy
    img_array = np.load(npy_path)
    
    # Créer une image colorée (Rouge pour classe 1, Noir sinon)
    colored_img = np.zeros((*img_array.shape, 3), dtype=np.uint8)
    colored_img[img_array == 1] = [255, 0, 0]  # Rouge
    colored_img[img_array != 1] = [0, 0, 0]    # Noir
    
    # Sauvegarder l'image PNG
    output_png = f"{file}/{nuts3}/{year}/{filename.replace('.npy', '.png')}"
    Image.fromarray(colored_img).save(output_png)
    print(f"Image sauvegardée : {output_png}")

    # Retourne un masque binaire (1 = rouge, 0 = noir)
    return (img_array == 1).astype(np.uint8)

# Charger et stocker les masques pour chaque année
for year in years:
    masks[year] = process_year(year)

# --- Étape 5 : Calcul de la différence entre 2018 et 2021 ---
mask_2018 = masks[2018]
mask_2021 = masks[2021]

# Création de l'image de différence
diff_img = np.zeros((*mask_2018.shape, 3), dtype=np.uint8)

# Appliquer les couleurs en fonction des différences
diff_img[(mask_2018 == 0) & (mask_2021 == 0)] = [200, 200, 200]  # Gris clair (0-0)
diff_img[(mask_2018 == 1) & (mask_2021 == 1)] = [255, 150, 150]  # Rouge clair (1-1)
diff_img[(mask_2018 == 0) & (mask_2021 == 1)] = [150, 0, 0]       # Rouge foncé (0-1)
diff_img[(mask_2018 == 1) & (mask_2021 == 0)] = [0, 0, 150]       # Bleu foncé (1-0)

# Sauvegarder l'image de différence
diff_output = f"{file}/{nuts3}/diff_{filename.replace('.npy', '.png')}"
Image.fromarray(diff_img).save(diff_output)
print(f"Image de différence sauvegardée : {diff_output}")
