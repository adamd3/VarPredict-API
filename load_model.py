import logging
import pandas as pd
import pickle

try:
    with open('./model_data/best_models.pkl', 'rb') as file:
        best_models = pickle.load(file)
except FileNotFoundError:
    logging.error("Failed to load best_models.pkl")
    best_models = {}

try:
    with open('./model_data/metadata.txt', 'rb') as file:
        meta_data = pd.read_csv(file, sep='\t')
except FileNotFoundError:
    logging.error("Failed to load metadata")
    meta_data = pd.DataFrame()

try:
    sample_genotypes = pd.read_csv('./model_data/sample_genotypes.tsv', sep='\t')
except FileNotFoundError:
    logging.error("Failed to load sample_genotypes.tsv")
    sample_genotypes = pd.DataFrame()
