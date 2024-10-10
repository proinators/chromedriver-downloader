"""To build this file, use the following command in the parent directory:
python -m zipapp chromedriverdownloader/ -o chromedriver_downloader.pyz -c"""

import warnings
warnings.filterwarnings('ignore')

from modules import requests
from sys import argv

import json
import zipfile
import os
import tempfile
import shutil


def download_and_unzip_chromedriver(json_data, output_path):
    data = json.loads(json_data)
    
    chromedriver_url = next(
        item['url'] for item in data['channels']['Stable']['downloads']['chromedriver']
        if item['platform'] == 'win64'
    )
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, 'chromedriver.zip')
        response = requests.get(chromedriver_url)
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        chromedriver_path = None
        for root, dirs, files in os.walk(temp_dir):
            if 'chromedriver.exe' in files:
                chromedriver_path = os.path.join(root, 'chromedriver.exe')
                break
        
        if not chromedriver_path:
            raise FileNotFoundError("chromedriver.exe not found in the downloaded package")
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Copy chromedriver.exe to the output path
        destination = os.path.join(output_path, 'chromedriver.exe')
        shutil.copy2(chromedriver_path, destination)
    
    print(f"ChromeDriver has been downloaded and extracted to: {output_path}")

def fetch_json_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        exit(1)



api_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

print("Fetching the latest version")
json_data = fetch_json_data(api_url)

output_path = argv[1]

print("Starting the download...")	

download_and_unzip_chromedriver(json_data, output_path)

input("Press ENTER to continue...")

