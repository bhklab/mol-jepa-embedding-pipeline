import sys
import pandas as pd
from damply import dirs


colData = pd.read_csv(dirs.RAWDATA / "HDD/colData.tsv",sep="\t",low_memory=False)
toxData = pd.read_csv(dirs.RAWDATA / "HDD/Tox21.tsv",sep="\t")

CHECK_COLS = ["ATC.Code",
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
             "DICT.Keywords"]


mol_universe = set()
for col in CHECK_COLS:
    temp = colData.dropna(subset=col)

    if col == "FDA.Approved":
        # The 'check missing' approach doesn't work, here we have to select
        # for exactly true 
        temp = temp[temp[col]==True]
    mol_universe = mol_universe.union(set(temp['HDD.Compound.ID']))
    



tox_mols = toxData.columns[1:]
mol_universe = mol_universe.union(set(tox_mols))



mol_universe = sorted(list(mol_universe))

print(f"After taking the full union, the number of molecules is: {len(mol_universe)}")

with open(dirs.PROCDATA / "mol_counts.txt","w") as ostream:
    ostream.writelines((f"After taking the full union, the number of molecules is {len(mol_universe)}"))


with open(dirs.PROCDATA / "molecule_universe.txt",'w') as ostream:
    ostream.writelines([x+"\n" for x in mol_universe])



