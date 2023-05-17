from fastapi import FastAPI, UploadFile
import pandas as pd
import pickle
import logging

app = FastAPI()

try:
    with open('best_models.pkl', 'rb') as file:
        best_models = pickle.load(file)
except FileNotFoundError:
    logging.error("Failed to load best_models.pkl")
    best_models = {}

try:
    sample_genotypes = pd.read_csv("sample_genotypes.csv")
except FileNotFoundError:
    logging.error("Failed to load sample_genotypes.csv")
    sample_genotypes = pd.DataFrame()

class GenotypesData:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @classmethod
    def from_file(cls, file: UploadFile):
        df = pd.read_csv(file.file)
        return cls(df)

    def validate_columns(self):
        input_columns = set(self.data.columns)
        sample_columns = set(sample_genotypes.columns)
        return input_columns == sample_columns

    def preprocess_data(self):
        preprocessed_data = self.data
        return preprocessed_data


@app.post("/predict/")
def predict_gene_expression(genotypes_data: GenotypesData):
    if not genotypes_data.validate_columns():
        return {"message": "Invalid columns"}

    feature_id = genotypes_data.data.columns[0]

    if feature_id not in best_models:
        return {"message": "Feature not found"}

    model = best_models[feature_id]

    input_data = genotypes_data.preprocess_data()

    try:
        predictions = model.predict(input_data)
    except Exception as e:
        logging.error(f"Prediction failed: {str(e)}")
        return {"message": "Prediction failed"}

    return {"predictions": predictions.tolist()}


logging.basicConfig(level=logging.ERROR, filename="api.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")
