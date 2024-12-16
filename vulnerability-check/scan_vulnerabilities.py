import os
import json
import subprocess

def scan_image(image):
    """Scan a Docker image using Trivy and return the vulnerability data."""
    try:
        print(f"Scanning image: {image}")
        result = subprocess.run(
            ['trivy', 'image', '--format', 'json', image], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error scanning {image}: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for {image}: {e}")
        return None

def main():
    try:
        with open('docker_images.txt', 'r') as f:
            images = [line.strip() for line in f if line.strip()]

        results = []
        for image in images:
            result = scan_image(image)
            if result is not None:
                results.append(result)

        with open('vulnerabilities.json', 'w') as f:
            json.dump({'jsonResults': results}, f, indent=2)

        print(f"Scanned {len(results)} images. Results saved to vulnerabilities.json")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
