import sys
from transformers import AutoModel
import pandas as pd
from damply import dirs
from collections import defaultdict
import tqdm 
import yaml
import torch 


with open(dirs.CONFIG / "embeddings.yaml", 'r') as file:
    # Load the contents safely
    model_params = yaml.safe_load(file)



device = model_params['PARAMETERS']['device']

if device == "auto":
    device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
else: 
    device = device

model = AutoModel.from_pretrained("Flogrammer/Mol-JEPA", trust_remote_code=True)


model.to(device)
model.eval()


with open(dirs.PROCDATA /"molecule_universe.txt","r") as istream:
    mol_universe = istream.readlines()
    mol_universe = [x.rstrip() for x in mol_universe]


drug_data = pd.read_csv(dirs.RAWDATA / "HDD"/ "colData.tsv",sep="\t", usecols=["HDD.Compound.ID", "Pubchem.CID","SMILES"])
drug_data = drug_data.dropna(subset=["SMILES","Pubchem.CID"])

drug_data = drug_data[drug_data['HDD.Compound.ID'].isin(mol_universe)]


mol_embeddings = defaultdict(list)
failed = 0

for _, row in tqdm.tqdm(drug_data.iterrows(), total=len(drug_data)):
    compound_id = row["HDD.Compound.ID"]
    try:
        out = model([row["SMILES"]])
    except ValueError as exc:
        failed += 1
        print(f"{compound_id}: {exc}", file=sys.stderr)
        continue

    embedding = out.cls.cpu().numpy().squeeze()
    mol_embeddings["HDD.Compound.ID"].append(compound_id)
    mol_embeddings["Pubchem.CID"].append(int(row["Pubchem.CID"]))
    for i, value in enumerate(embedding, start=1):
        mol_embeddings[f"Emb-{i}"].append(value)

count = len(mol_embeddings["HDD.Compound.ID"])
print(f"Generated {count} embeddings from {len(drug_data)} eligible compounds ({failed} failed).")
if not count:
    raise SystemExit("No valid compound embeddings were generated.")

pd.DataFrame(mol_embeddings).to_csv(dirs.RESULTS / "molecule_embeddings.csv")
