import requests
import s3fs

fs = s3fs.S3FileSystem(
    client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
    key = os.environ["AWS_ACCESS_KEY_ID"], 
    secret = os.environ["AWS_SECRET_ACCESS_KEY"]
    )

fs.ls("projet-hackathon2025")
# URL de l'API
url = "https://hackathon-ntts-2025.lab.sspcloud.fr/predict_image"

# Chemin vers l'image que tu veux tester
file = 'projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/UKJ22/2018/250/3615590_3131740_0_375.tif'
response = requests.get(url, params={'image': file})

# Vérifier la réponse de l'API
if response.status_code == 200:
    print("Réponse de l'API :")
    print(response.json())  # Affiche la réponse JSON retournée par l'API
else:
    print(f"Erreur {response.status_code}: {response.text}")


url = "https://hackathon-ntts-2025.lab.sspcloud.fr/predict_nuts"

# Chemin vers l'image que tu veux tester
file = 'projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/UKJ22/2018/250/3615590_3131740_0_375.tif'
response = requests.get(url, params={'image': file})

# Vérifier la réponse de l'API
if response.status_code == 200:
    print("Réponse de l'API :")
    print(response.json())  # Affiche la réponse JSON retournée par l'API
else:
    print(f"Erreur {response.status_code}: {response.text}")
