import json
import pandas as pd
import numpy as np
from collections import Counter
from tqdm import tqdm
import os

# Paths
downstream_data_path = '/home/hngoc/gin/Clinical-Note-Extraction/data/Timeline'
ADMISSION_NODES_PATH = os.path.join(downstream_data_path, 'admission_nodes.json')
TRAIN_DF_PATH        = os.path.join(downstream_data_path, 'models', 'train_df.csv')
DRUG_VOCAB_PATH      = os.path.join(downstream_data_path, 'top50_drug_vocab.json')
DRUG_WEIGHTS_PATH    = os.path.join(downstream_data_path, 'drug_rec_pos_weights.npy')

print("Loading admission nodes...")
with open(ADMISSION_NODES_PATH) as f:
    admission_nodes = json.load(f)

print("Loading train_df...")
train_df = pd.read_csv(TRAIN_DF_PATH)
train_ids = train_df['id'].astype(str).tolist()

print(f"Number of training admissions: {len(train_ids)}")

# Count drugs in training set
drug_counter = Counter()
for adm_id in tqdm(train_ids, desc="Counting drugs"):
    # Handle possible float IDs in CSV vs string keys in JSON
    if '.' in adm_id:
        adm_id = str(int(float(adm_id)))
    
    adm_data = admission_nodes.get(adm_id)
    if adm_data:
        drugs = [d.lower() for d in adm_data.get('drugs', []) if d]
        drug_counter.update(drugs)

print(f"Total unique drugs found: {len(drug_counter)}")

# Get top 50 drugs
top_50_drugs = [d for d, count in drug_counter.most_common(50)]
drug_to_idx = {drug: i for i, drug in enumerate(top_50_drugs)}

print("Top 5 drugs:", top_50_drugs[:5])

# Save vocab
with open(DRUG_VOCAB_PATH, 'w') as f:
    json.dump(drug_to_idx, f, indent=2)
print(f"Saved vocab to {DRUG_VOCAB_PATH}")

# Compute pos_weights
# pos_weight = n_negative / n_positive
n_train = len(train_ids)

pos_weights = np.zeros(50, dtype=np.float32)
drug_counts = np.zeros(50)

for adm_id in tqdm(train_ids, desc="Calculating weights"):
    if '.' in adm_id:
        adm_id = str(int(float(adm_id)))
    
    adm_data = admission_nodes.get(adm_id)
    if adm_data:
        drugs = set([d.lower() for d in adm_data.get('drugs', []) if d])
        for drug, idx in drug_to_idx.items():
            if drug in drugs:
                drug_counts[idx] += 1

for i in range(50):
    n_pos = drug_counts[i]
    n_neg = n_train - n_pos
    if n_pos > 0:
        pos_weights[i] = n_neg / n_pos
    else:
        pos_weights[i] = 1.0 # Should not happen for top 50

# Save weights
np.save(DRUG_WEIGHTS_PATH, pos_weights)
print(f"Saved pos_weights to {DRUG_WEIGHTS_PATH}")
