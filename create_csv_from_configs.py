import os
import json
import pandas as pd
from collections import defaultdict
import argparse

def extract_replica_counts(json_dir, output_csv):
    # Collect all load_X_config.json files
    json_files = sorted(
        [f for f in os.listdir(json_dir) if f.startswith("load_") and f.endswith("_config.json")],
        key=lambda x: int(x.split("_")[1])
    )

    # Initialize dictionary to store service replica data
    replica_data = defaultdict(dict)

    # Process each file
    for json_file in json_files:
        load_value = int(json_file.split("_")[1])
        with open(os.path.join(json_dir, json_file), "r") as f:
            config = json.load(f)
            service_replica_count = defaultdict(int)
            for dep in config["deployments"]:
                service_replica_count[dep["name"]] += dep["replicas"]
            for service, count in service_replica_count.items():
                replica_data[service][load_value] = count

    # Convert to DataFrame
    df = pd.DataFrame(replica_data).T.sort_index()
    df = df.reindex(sorted(df.columns), axis=1)

    # Save to CSV
    df.to_csv(output_csv)
    print(f"Replica summary saved to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Extract microservice replica counts from JSON config files.")
    parser.add_argument("--json-dir", type=str, required=True, help="Path to the directory containing load_*.json files")
    parser.add_argument("--output", type=str, required=True, help="Path to the output CSV file")
    args = parser.parse_args()

    extract_replica_counts(args.json_dir, args.output)

if __name__ == "__main__":
    main()
