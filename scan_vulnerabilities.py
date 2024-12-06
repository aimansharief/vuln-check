import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read docker images from file
def read_docker_images(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Scan vulnerabilities using Trivy
def scan_vulnerabilities(image_name):
    try:
        result = subprocess.run(['trivy', 'image', '--quiet', '--no-progress', image_name], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f'Error scanning {image_name}: {e.stderr}')
        return f'Error scanning {image_name}: {e.stderr}'

# Main function to scan all images and store results
def main():
    images = read_docker_images('/Users/admin/Documents/workspace/vuln-check/docker_images.txt')
    with open('scan_results.txt', 'w') as result_file:
        for image in images:
            logging.info(f'Scanning {image}...')
            scan_result = scan_vulnerabilities(image)
            
            # Extract summary from scan_result
            summary_line = next((line for line in scan_result.splitlines() if line.startswith('Total:')), 'No vulnerabilities found')
            
            # Write image name and summary to file
            result_file.write(f'Image: {image}\n')
            result_file.write(f'{summary_line}\n')
            result_file.write('\n' + '='*40 + '\n')

if __name__ == '__main__':
    main()
