import argparse

from utils import concatenate_gpkg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concatene predictions pipeline")
    parser.add_argument("--year", type=int, required=True, help="year (e.g., 2024)")
    args = parser.parse_args()

    concatenate_gpkg(args.year)
