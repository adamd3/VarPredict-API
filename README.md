# VarPredict-API

![VarPredict-API](https://github.com/adamd3/VarPredict-API/actions/workflows/deploy.yml/badge.svg)

This is an API for the [VarPredict](https://github.com/adamd3/VarPredict/)
package. It allows one to query the model to predict gene expression given a
set of genetic variants.

## Usage

The API accepts a table of genotypes as input (see example data), which it uses
to predict the expression levels of 4,736 genes in Pseudomonas aeruginosa. The
underlying models for were trained using a dataset of 407 strains during
Planktonic growth. The data are described in
[this paper](https://www.embopress.org/doi/full/10.15252/emmm.201910264).

## Example data

See `model_data/sample_genotypes.tsv` for sample genotype data that can be used
to extract expression predictions for available genes. The expression values
returned are for the genes which are keys in the `model_data/best_models.pkl`
dictionary.
