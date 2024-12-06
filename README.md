# Vulnerability Scanning with Trivy

This project provides a script to scan Docker images for vulnerabilities using Trivy, a comprehensive and easy-to-use vulnerability scanner for containers.

## Usage

1. **Prepare the Docker Images List**:
   - Create a text file named `docker_images.txt` in the same directory as the script.
   - Add the Docker image names you want to scan to the `docker_images.txt` file, one per line.

2. **Run the Script**:
   - Execute the `scan_vulnerabilities.py` script to start the scanning process.
   - Run the following command in your terminal:
     ```bash
     python scan_vulnerabilities.py
     ```
   - The script will read the image names from `docker_images.txt`, scan each image using Trivy, and save the results in `scan_results.txt`.

## Requirements

- Python 3.x
- Trivy installed and accessible in your system's PATH.

## Setup

1. **Install Trivy**:
   - Follow the [Trivy installation guide](https://aquasecurity.github.io/trivy/v0.18.3/installation/) to set up Trivy on your system.

2. **Install Python**:
   - Ensure Python 3.x is installed on your system.

## License

This project is licensed under the MIT License.
