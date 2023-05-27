import requests

def test_predict_gene_expression(file_path):
    file_path = "./model_data/sample_genotypes.tsv"
    url = "http://localhost:80/predict/"  
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    response_json = response.json()

    assert response.status_code == 200

    print(response_json)


if __name__ == "__main__":
    test_predict_gene_expression()