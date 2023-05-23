import requests
import json

def test_predict_gene_expression(file_path):
    url = "http://localhost:8000/predict/"  
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    print(response.json())

test_predict_gene_expression("./model_data/sample_genotypes.tsv")