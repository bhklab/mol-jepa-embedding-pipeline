# Mol-JEPA Embedding Pipeline

**Authors:** [James Bannon](https://github.com/jbannon), Michael Tran, Matthew Boccalon

**Contact:** [bhklab.jamesbannon@gmail.com](mailto:bhklab.jamesbannon@gmail.com)

**Description:** Pipeline for Generating Mol-JEPA Embeddings from HDD Compounds

--------------------------------------

[![pixi-badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json&style=flat-square)](https://github.com/prefix-dev/pixi)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/mkdocs--material-gray?logo=materialformkdocs&style=flat-square)](https://github.com/squidfunk/mkdocs-material)

![GitHub last commit](https://img.shields.io/github/last-commit/bhklab/mol-jepa-embedding-pipeline?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/bhklab/mol-jepa-embedding-pipeline?style=flat-square)
![GitHub pull requests](https://img.shields.io/github/issues-pr/bhklab/mol-jepa-embedding-pipeline?style=flat-square)
![GitHub contributors](https://img.shields.io/github/contributors/bhklab/mol-jepa-embedding-pipeline?style=flat-square)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/bhklab/mol-jepa-embedding-pipeline?style=flat-square)


This pipeline produces embeddings based on the pre-trained [Mol-JEPA architecture](https://arxiv.org/abs/2608.22642). The pipeline functions by downloading data from the Harmonized Drug Dataset ([HDD version 3.1](https://www.orcestra.ca/annotations/6ae4fc5833e1ba54a5335fda)), selecting a compound universe of compounds with at least some labeled data, and using the pre-trained Mol-JEPA Architecture to produce the embeddings based on the compound's [SMILES](https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_System) string. 

Concretely, for constructing the drug universe we only keep molecules which are either:
- In the Tox21 dataset 

Or

- have non-missing entry for at least one of the following columns in the HDD file `coldata.tsv`: 
```bash
"ATC.Code",
"Mechanism.of.Action",
"FDA.Approved",
'BBB.Permeable',
"LTKB.DILI.Annotation"	,
"DILIrank.DILI.Severity.Grade",
"DILIrank.DILI.Annotation",
"DILIst.DILI.Annotation",
"Livertox.Hepatotoxicity.Likelihood.Score",
"Livertox.Hepatotoxicity.Likelihood.Reason",
"DIRIL.Label.Gong",
"DIRIL.Label.Shi",
"DIRIL.Toxicity",
"DICT.Cardiotoxicity",
"DICT.Label.Section",
"LTKB.DILI.Severity.Grade",
"DICT.Concern",
"DICT.Keywords"`
```
The code here can be run locally and also as a [Nextflow](https://www.nextflow.io) pipeline.


# Running Locally


Pixi is required to run this project. If you haven't installed it yet, [follow these instructions](https://pixi.sh/latest/). Once you've done follow these steps:

1. Clone this repository to your local machine
2. Navigate to the project directory
3. Set up the environment using Pixi:

```bash
pixi install
```

Next navigate to `workflow/scripts` and run the folowing commands in order:

1. `pixi run "python3 download.py"`
2. `pixi run "python3 construct_drug_universe.py"`
3. `pixi run "python3 generate_embeddings.py"`


This will put the resulting embeddings in the `data/results` folder. 


# Running with Nextflow