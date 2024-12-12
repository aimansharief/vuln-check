import os
import json
import subprocess

def scan_image(image):
    """Scan a Docker image using Trivy and return the vulnerability data."""
    try:
        # Run Trivy scan with JSON output
        result = subprocess.run(
            ['trivy', 'image', '--format', 'json', image], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error scanning {image}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error parsing JSON for {image}")
        return None

def main():
    # Read images from docker_images.txt
    with open('docker_images.txt', 'r') as f:
        images = [line.strip() for line in f]

    # Prepare results list
    results = []

    # Scan each image
    for image in images:
        print(f"Scanning {image}...")
        scan_result = scan_image(image)
        if scan_result:
            # Add the target to the result for tracking
            scan_result['Target'] = image
            results.append(scan_result)

    # Save results to vul.json
    with open('vul.json', 'w') as f:
        json.dump({'jsonResults': results}, f, indent=2)

    print(f"Scanned {len(results)} images. Results saved to vul.json")

if __name__ == '__main__':
    main()
