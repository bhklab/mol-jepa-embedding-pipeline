import matplotlib.pyplot as plt
import seaborn as sns
import umap
import pandas as pd
from damply import dirs
import os 
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import re
from sklearn.cluster import SpectralClustering


with open("keep_mols.txt","r") as istream:
    keep_mols = istream.readlines()
    keep_mols = [x.rstrip() for x in keep_mols]

data = pd.read_csv(dirs.RESULTS / "molecule_embeddings.csv",index_col=0)
emb_cols = data.columns[2:]
# print(data.columns)
# sys.exit()
def process_atc_code(code_string: str, level: int = 4) -> str:
    """Return the requested ATC hierarchy level (for example N03AX09 -> N03A)."""
    result = re.findall(r"[a-zA-Z]|[^a-zA-Z]+", code_string)
    return "".join(result[:level])


colData = pd.read_csv(dirs.RAWDATA / "HDD/colData.tsv",
                      sep="\t",
                      usecols =  ["HDD.Compound.ID", "Pubchem.CID", "Mechanism.of.Action","ATC.Code","BBB.Permeable",
                                  "LTKB.DILI.Severity.Grade",
                                  "LTKB.DILI.Annotation",
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
                                  "DICT.Concern", 
                                  "DICT.Keywords",
                                  "BBB.Permeable"])


print(colData["DILIrank.DILI.Severity.Grade"].value_counts())
print(colData["DILIrank.DILI.Annotation"].value_counts())

