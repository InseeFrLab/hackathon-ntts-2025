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
import requests
import json
file = 'projet-hackathon-ntts-2025/data-preprocessed/patchs/CLCplus-Backbone/SENTINEL2/UKJ22/2018/250/3615590_3131740_0_375.tif'
response = requests.get(url, params={'nuts_id':"BE100","year": "2024"})
predictions =json.loads(response.json()['predictions'])

# Extraire les features
features = predictions["features"]

# Convertir en DataFrame
df = pd.json_normalize(features)

# Convertir les coordonnées en géométrie (shapely)
df["geometry"] = df["geometry.coordinates"].apply(lambda x: shape({"type": "Polygon", "coordinates": x}))
del df["geometry.coordinates"]
del df["geometry.type"]

# Créer un GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")  # Ajuster le CRS si nécessaire

# Supprimer les colonnes inutiles
gdf = gdf.drop(columns=["geometry.coordinates", "type", "geometry.type"])

# Renommer les colonnes pour plus de clarté
gdf = gdf.rename(columns={"id": "ID", "properties.label": "Label"})

# Vérifier la réponse de l'API
if response.status_code == 200:
    print("Réponse de l'API :")
    print(response.json())  # Affiche la réponse JSON retournée par l'API
else:
    print(f"Erreur {response.status_code}: {response.text}")


# pyplot
import matplotlib.pyplot as plt

# Create a plot
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, column="Label", cmap="Set1", edgecolor="black", legend=True)

# Set title
ax.set_title("GeoDataFrame Plot", fontsize=14)

# Save the figure as a PNG file
plt.savefig("geodataframe_plot.png", dpi=300, bbox_inches="tight")  # High resolution

# Show the plot (optional)
plt.show()

#
# Show the plot (optional)

import folium


# Ensure gdf has the correct CRS before transforming
gdf = gdf.set_crs("EPSG:3035",allow_override=True)  # Set original CRS if not defined

# Convert to EPSG:4326 (WGS 84)
gdf = gdf.to_crs("EPSG:4326")


centroid = gdf.geometry.unary_union.centroid
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles="OpenStreetMap")  # OSM as background

# Add polygons to the map
for _, row in gdf.iterrows():
    folium.GeoJson(
        row.geometry,
        style_function=lambda feature: {
            "fillColor": "blue",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.5,
        },
        tooltip=f"ID: {row['ID']}, Label: {row['Label']}"
    ).add_to(m)

# Save to an HTML file
m.save("geodataframe_map.html")

print("✅ Map saved as geodataframe_map.html")

