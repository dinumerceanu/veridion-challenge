import pandas as pd

file_path = r"D:\veridion\veridion-challenge\logos.snappy.parquet"

df = pd.read_parquet(file_path)

url_column = "domain"
urls = df[url_column].tolist()

for i in range(5):
    print(urls[i])
