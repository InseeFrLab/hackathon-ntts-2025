import argparse
import time
import requests


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict nuts pipeline")
    parser.add_argument("--nuts3", type=str, required=True, help="NUTS3 (e.g., 'BE100')")
    parser.add_argument("--year", type=int, required=True, help="year (e.g., 2024)")
    args = parser.parse_args()

    nuts3 = args.nuts3
    year = args.year

    start_time = time.time()

    print(f"Start of the prediction of NUTS {nuts3}")
    url = "https://funathon-2026-project3-api.lab.sspcloud.fr/predict_nuts"
    response = requests.get(url, params={"nuts_id": nuts3, "year": year})

    if response.status_code == 200:
        print("Prediction done, now register on s3 cache")
    else:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")
