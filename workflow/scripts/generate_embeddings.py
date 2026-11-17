import sys
from transformers import AutoModel
import pandas as pd
from damply import dirs
from collections import defaultdict
import tqdm 
import functools
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


# necessary wrapper to catch errors
def safe_forward_wrapper(original_forward):
    @functools.wraps(original_forward)
    def wrapped_forward(*args, **kwargs):
        try:
            return original_forward(*args, **kwargs)
        except ValueError as e:
            # print(f"⚠️ Transform ValueError intercepted in forward pass: {e}")
            # Return None or a dummy ModelOutput object depending on downstream needs
            return None
    return wrapped_forward



model.forward = safe_forward_wrapper(model.forward)
model.to(device)
model.eval()


with open(dirs.PROCDATA /"molecule_universe.txt","r") as istream:
    mol_universe = istream.readlines()
    mol_universe = [x.rstrip() for x in mol_universe]


drug_data = pd.read_csv(dirs.RAWDATA / "HDD"/ "colData.tsv",sep="\t", usecols=["HDD.Compound.ID", "Pubchem.CID","SMILES"])
drug_data = drug_data.dropna(subset=["SMILES","Pubchem.CID"])

drug_data = drug_data[drug_data['HDD.Compound.ID'].isin(mol_universe)]


mol_embeddings = defaultdict(list)

for idx, row in tqdm.tqdm(drug_data.iterrows(),total = drug_data.shape[0]):
    mol = row['SMILES']
    
    out = model([mol])
    
    if out is not None:
        embedding = out.cls.cpu().numpy().squeeze()

        mol_embeddings["HDD.Compound.ID"].append(row["HDD.Compound.ID"])
        mol_embeddings["Pubchem.CID"].append(int(row["Pubchem.CID"]))
    
        for i in range(len(embedding)):
            mol_embeddings[f'Emb-{i+1}'].append(embedding[i])
    
    
mol_embeddings = pd.DataFrame(mol_embeddings)
mol_embeddings.to_csv(dirs.RESULTS / "molecule_embeddings.csv")

    

