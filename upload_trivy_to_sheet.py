import json
import csv
import os
import re

# Load JSON data
with open("vul.json", "r") as file:
    data = json.load(file)

# Extract results from jsonResults
results = data.get("jsonResults", [])

# Define headers
headers = ["Image","Library", "Vulnerability ID", "Severity", "Status", "Installed Version", "Fixed Version", "Title"]

def sanitize_filename(name):
    """
    Sanitize the filename by removing or replacing problematic characters
    and ensuring it's a valid filename.
    """
    # Replace problematic characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove leading/trailing spaces and periods
    sanitized = sanitized.strip('. ')
    # Limit filename length if needed
    return sanitized[:255]

# Create a single directory to store all CSV files
base_directory = os.path.join(os.getcwd(), "vulnerability_reports")
os.makedirs(base_directory, exist_ok=True)

# Iterate through each result and create or append to CSV files for relevant Targets
for result in results:
    artifact_name = result.get("ArtifactName", "unknown_artifact")

    # Sanitize artifact name for filename
    sanitized_artifact_name = sanitize_filename(artifact_name)

    # Create CSV filename in the base directory
    csv_filename = os.path.join(base_directory, f"{sanitized_artifact_name}.csv")

    # Check if file exists to determine if headers need to be written
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write headers only if the file is new
        if not file_exists:
            writer.writerow(headers)

        for entry in result.get("Results", []):
            target = entry.get("Target", "Unknown")

            # Consider only targets with Java, Python, or Node.js
            if not any(lang in target for lang in ["Java", "Python", "Node.js"]):
                continue

            # Get vulnerabilities from the current Results entry
            vulnerabilities = entry.get("Vulnerabilities", [])

            if not vulnerabilities:
                continue

            # Write vulnerability details
            for vuln in vulnerabilities:
                writer.writerow([
                    artifact_name,
                    vuln.get("PkgName", ""),
                    vuln.get("VulnerabilityID", ""),
                    vuln.get("Severity", ""),
                    vuln.get("Status", ""),
                    vuln.get("InstalledVersion", ""),
                    vuln.get("FixedVersion", ""),
                    vuln.get("Title", "")
                ])

        print(f"Added vulnerability report for {artifact_name} to {csv_filename}")
