import json
import csv
import os
import re
import pandas as pd

with open("vulnerabilities.json", "r") as file:
    data = json.load(file)

results = data.get("jsonResults", [])

headers = ["Image", "Target", "Library", "Vulnerability ID", "Severity", "Status", "Installed Version", "Fixed Version", "Title"]

def sanitize_filename(name):
    """
    Sanitize the filename by removing or replacing problematic characters
    and ensuring it's a valid filename.
    """
    # Replace problematic characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove leading/trailing spaces and periods
    sanitized = sanitized.strip('. ')
    return sanitized[:255]

# Create a single directory to store all CSV files
base_directory = os.path.join(os.getcwd(), "vulnerability_reports")
os.makedirs(base_directory, exist_ok=True)

for result in results:
    artifact_name = result.get("ArtifactName", "unknown_artifact")

    # Sanitize artifact name for filename
    sanitized_artifact_name = sanitize_filename(artifact_name)
    csv_filename = os.path.join(base_directory, f"{sanitized_artifact_name}.csv")
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(headers)

        for entry in result.get("Results", []):
            target = entry.get("Target", "Unknown")

            vulnerabilities = entry.get("Vulnerabilities", [])

            if not vulnerabilities:
                continue

            for vuln in vulnerabilities:
                writer.writerow([
                    artifact_name,
                    target,
                    vuln.get("PkgName", ""),
                    vuln.get("VulnerabilityID", ""),
                    vuln.get("Severity", ""),
                    vuln.get("Status", ""),
                    vuln.get("InstalledVersion", ""),
                    vuln.get("FixedVersion", ""),
                    vuln.get("Title", "")
                ])

        print(f"Added vulnerability report for {artifact_name} to {csv_filename}")

def merge_csv_files(directory_path, output_file="merged_vulnerabilities.csv"):
    dataframes = []

    for file in os.listdir(directory_path):
        if file.endswith(".csv"):
            file_path = os.path.join(directory_path, file)
            df = pd.read_csv(file_path)
            dataframes.append(df)
    merged_df = pd.concat(dataframes, ignore_index=True)

    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved to {output_file}")

merge_csv_files(base_directory)
