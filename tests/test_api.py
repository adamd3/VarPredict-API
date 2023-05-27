import pytest
import requests

@pytest.fixture
def file_path():
    return "./model_data/sample_genotypes.tsv"

def test_predict_gene_expression(file_path):
    url = "13.53.42.163:80/predict/"  
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    response_json = response.json()

    assert response.status_code == 200

    print(response_json)


if __name__ == "__main__":
    test_predict_gene_expression()