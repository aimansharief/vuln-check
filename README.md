# Docker Image Vulnerability Scanner

This project provides a comprehensive solution for scanning Docker images for vulnerabilities using Trivy and generating detailed reports in both JSON and CSV formats.

## Usage

1. **Docker Registry Login**:
   - Before scanning, make sure you're logged into the required Docker registries:
     ```bash
     # For Docker Hub
     docker login
     
     # For private registries (like Azure Container Registry)
     docker login <registry-url>
     # Example: docker login sunbirded.azurecr.io
     ```
   - This step is essential for accessing private repositories and avoiding rate limits

2. **Prepare the Docker Images List**:
   - Add the Docker image names you want to scan to the `docker_images.txt` file, one per line.
   Example: 
   ```
   docker.io/bitnami/redis:7.4.1
   docker.io/grafana/grafana:11.4.0
   docker.io/library/busybox:1.31.1
   ```

3. **Run the Script**:
   - Execute the `scan_vulnerabilities.py` script to start the scanning process.
     ```bash
     python scan_vulnerabilities.py
     ```
   - Execute the `upload_trivy_to_sheet.py` script to upload the results to a csv file.
     ```bash
     python upload_trivy_to_sheet.py
     ```

4. **Cleanup Before Re-scanning**:
   - Before running a new scan, make sure to remove the previous scan results:
     ```bash
     rm vulnerabilities.json           # Remove the JSON results file
     rm -rf vulnerability_reports/     # Remove the directory containing CSV reports
     ```
   - This cleanup step is important to avoid mixing old and new scan results

## Requirements

- Python 3.x
- Trivy installed and accessible in your system's PATH.
- Docker CLI installed and configured

## Setup

1. **Install Trivy**:
   - Follow the [Trivy installation guide](https://aquasecurity.github.io/trivy/v0.18.3/installation/) to set up Trivy on your system.

2. **Install Python**:
   - Ensure Python 3.x is installed on your system.

