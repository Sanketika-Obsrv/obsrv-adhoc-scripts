# Docker Image Vulnerability Scanner

This project provides a comprehensive solution for scanning Docker images for vulnerabilities using Trivy and generating detailed reports in both JSON and CSV formats.

## Usage

1. **Prepare the Docker Images List**:
   - Add the Docker image names you want to scan to the `docker_images.txt` file, one per line.
   Example: 
   ```
   docker.io/bitnami/redis:7.4.1
   docker.io/grafana/grafana:11.4.0
   docker.io/library/busybox:1.31.1
   ```

2. **Run the Script**:
   - Execute the `scan_vulnerabilities.py` script to start the scanning process.
     ```bash
     python scan_vulnerabilities.py
     ```
   - Execute the `upload_trivy_to_sheet.py` script to upload the results to a csv file.
     ```bash
     python upload_trivy_to_sheet.py
     ```

## Requirements

- Python 3.x
- Trivy installed and accessible in your system's PATH.

## Setup

1. **Install Trivy**:
   - Follow the [Trivy installation guide](https://aquasecurity.github.io/trivy/v0.18.3/installation/) to set up Trivy on your system.

2. **Install Python**:
   - Ensure Python 3.x is installed on your system.

