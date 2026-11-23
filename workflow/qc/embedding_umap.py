import matplotlib.pyplot as plt
import seaborn as sns
import umap
import pandas as pd
from damply import dirs
import os 
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import re

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
                      usecols =  ["HDD.Compound.ID", "Pubchem.CID", "Mechanism.of.Action","ATC.Code","BBB.Permeable"])




reducer = umap.UMAP(random_state=42)
data = data.merge(colData, on="HDD.Compound.ID")
data = data.dropna(subset=['Mechanism.of.Action','ATC.Code'])
data['ATC.Code']=[process_atc_code(x,2) for x in data['ATC.Code']]

data = data[data['HDD.Compound.ID'].isin(keep_mols)]
X = data[emb_cols].values
# X = [["HS", "E0",  "E_inf", "EC50"]].values 
X = StandardScaler().fit_transform(X)
UM = reducer.fit_transform(X)
plot_df = pd.DataFrame({'UMAP-1':UM[:,0], 
                        'UMAP-2':UM[:,1],
                        'ATC':data['ATC.Code'].values})
ax =  sns.scatterplot(plot_df,x='UMAP-1',y='UMAP-2',hue='ATC',legend=True)
sns.move_legend(ax, "upper left", bbox_to_anchor=(1.02, 1))
plt.title(f"Mol-JEPA Embeddings vs. ATC Code")
plt.tight_layout()
plt.savefig(dirs.RESULTS / f"ATC_Mol-JEPA.png")
plt.close()


plot_df = pd.DataFrame({'UMAP-1':UM[:,0], 
                        'UMAP-2':UM[:,1],
                        'MOA':data['Mechanism.of.Action'].values})
ax =  sns.scatterplot(plot_df,x='UMAP-1',y='UMAP-2',hue='MOA',legend=True)

plt.title(f"Mol-JEPA Embeddings vs. MOA")
plt.tight_layout()
plt.savefig(dirs.RESULTS / f"MOA_Mol-JEPA.png")
plt.close()
