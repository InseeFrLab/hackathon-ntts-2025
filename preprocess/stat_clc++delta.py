import numpy as np
import pandas as pd
import s3fs

# Initialize S3 filesystem connection
fs = s3fs.S3FileSystem(
    client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Define directories and years
label_dir = "projet-hackathon-ntts-2025/data-preprocessed/labels/CLCplus-Backbone/SENTINEL2/"
years = ['2018', '2021']

# Get list of NUTS regions from S3
list_nuts = fs.ls(label_dir)

# Initialize results list
results = []

# Loop over NUTS regions
for nuts in list_nuts:
    print(nuts)
    nuts_path = nuts  # Full path to NUTS region
    nuts_id = nuts_path.split("/")[-1]  # Extract NUTS3 code from path

    for year in years:
        folder_path = f"{nuts_path}/{year}/250"

        # List all label files for this NUTS region and year
        try:
            folder = fs.ls(folder_path)
        except FileNotFoundError:
            continue  # Skip if no data for this year

        # Initialize counters
        total_ones = 0
        total_elements = 0

        # Loop over files
        for file_path in folder:
            with fs.open(file_path, "rb") as f:
                data = np.load(f)  # Load numpy file

            # Update counts
            total_ones += np.sum(data == 1)  # Count artificial pixels
            total_elements += data.size  # Total number of pixels

        # Compute artificialization ratio
        artificial_ratio = (total_ones / total_elements) * 100 if total_elements > 0 else 0

        # Store results
        results.append({"NUTS3": nuts_id, "year": year, "artificial_ratio": round(artificial_ratio, 2)})

# Convert results to DataFrame
df_results = pd.DataFrame(results)

# Pivot to get Artificialization Ratio for 2018 and 2021 in separate columns
df_pivot = df_results.pivot(index="NUTS3", columns="year", values="artificial_ratio")

# Rename columns
df_pivot.columns = [f"artificial_ratio_{year}" for year in df_pivot.columns]

# Reset index for readability
df_pivot.reset_index(inplace=True)

# Construct full S3 path
path_name_nuts="projet-hackathon-ntts-2025/indicators/NUTS2021.xlsx"

# Open the file using s3fs and read it with pandas
with fs.open(path_name_nuts, "rb") as f:
    df_label = pd.read_excel(f,1)

# Ensure column names are correct and standardized for merging
df_label.rename(columns={"Code 2021": "NUTS3","NUTS level 3": "name"}, inplace=True)
# Merge df_indicators with df_label on NUTS3
data = df_pivot.merge(df_label[["NUTS3","name"]], on="NUTS3", how="left")

data["artificial_ratio_evolution"]=np.round(100*(data["artificial_ratio_2021"]-data["artificial_ratio_2018"])/data["artificial_ratio_2018"],1)

data = data[["NUTS3","name","artificial_ratio_2018","artificial_ratio_2021","artificial_ratio_evolution"]]

data.to_parquet("indic_clc+.parquet", engine="pyarrow", index=False)

lpath =f"indic_clc+.parquet"
rpath =f"s3://projet-hackathon-ntts-2025/indicators/"

fs.put(lpath,rpath)
