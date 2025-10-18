import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

downloaded_logos = 0

def download_logo(domain):
    logo_url = f"https://img.logo.dev/{domains[i]}?token=pk_LeeVQnGLT3uD5zai-rFzVQ"
    global downloaded_logos
    folder = "logos"
    os.makedirs(folder, exist_ok=True)
    
    try:
        logo_response = requests.get(logo_url, timeout=2)
        logo_response.raise_for_status()

        content_type = logo_response.headers.get('Content-Type', '')
        if 'svg' in content_type:
            ext = 'svg'
        elif 'png' in content_type:
            ext = 'png'
        elif 'jpeg' in content_type or 'jpg' in content_type:
            ext = 'jpg'
        else:
            print("unknown extension")
            return

        file_name = f"{domain}.{ext}"
        file_path = os.path.join(folder, file_name)

        with open(file_path, 'wb') as f:
            f.write(logo_response.content)
            
        print(f"SAVED: Logo saved as {file_path}")
        downloaded_logos += 1

    except requests.exceptions.RequestException as e:
        print(f"ERROR: URL: {logo_url}: {e}")

file_path = r"D:\veridion\veridion-challenge\logos.snappy.parquet"

df = pd.read_parquet(file_path)

url_column = "domain"
domains = df[url_column].tolist()
timeout = 2

for i in range(100):
    download_logo(domains[i])

print(f"{downloaded_logos}/100")
