from fastapi import FastAPI, UploadFile, File
import logging
import pandas as pd
import pickle
import sklearn

app = FastAPI()

try:
    with open('./model_data/best_models.pkl', 'rb') as file:
        best_models = pickle.load(file)
except FileNotFoundError:
    logging.error("Failed to load best_models.pkl")
    best_models = {}

try:
    with open('./model_data/metadata.txt', 'rb') as file:
        meta_data = pd.read_csv(file, sep = '\t')
except FileNotFoundError:
    logging.error("Failed to load metadata")
    meta_data = pd.DataFrame()

try:
    sample_genotypes = pd.read_csv(
        './model_data/sample_genotypes.tsv', sep='\t')
except FileNotFoundError:
    logging.error("Failed to load sample_genotypes.tsv")
    sample_genotypes = pd.DataFrame()


class GenotypesData:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @classmethod
    def from_file(cls, file: UploadFile):
        df = pd.read_csv(file.file, sep="\t")
        return cls(df)

    def validate_columns(self):
        input_columns = set(self.data.columns)
        sample_columns = set(sample_genotypes.columns)
        return input_columns == sample_columns

    def preprocess_data(self):
        geno_list = (self.data)['feature_id'].tolist()
        genotypes_t = (self.data).iloc[:, 1:].transpose()
        genotypes_t.columns = geno_list 
        return genotypes_t


@app.post("/predict/")
def predict_gene_expression(file: UploadFile = File(...)):
    genotypes_data = GenotypesData.from_file(file)

    if not genotypes_data.validate_columns():
        return {"message": "Invalid columns"}

    genotypes_t = genotypes_data.preprocess_data()

    strain_list = list(genotypes_t.index.values)

    meta_sub = meta_data.dropna(how='all')
    meta_sub = meta_sub[meta_sub['sample_name'].isin(strain_list)]

    st_encod = pd.get_dummies(meta_sub['majority_ST'], prefix='ST')
    st_encod.index = strain_list

    vars_st = genotypes_t.merge(st_encod, left_index=True, right_index=True)

    X = vars_st.values
    scaler = sklearn.preprocessing.StandardScaler()
    X = scaler.fit_transform(X) 

    predictions_dict = {}

    for feature_id, model in best_models.items():
        try:
            predictions = model.predict(X)
            predictions_dict[feature_id] = predictions.tolist()
        except Exception as e:
            logging.error(f"Prediction failed: {str(e)} for {feature_id}")
            return {"message": "Prediction failed"}
        
    return predictions_dict


logging.basicConfig(level=logging.ERROR, filename="api.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
