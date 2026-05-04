import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from torch_geometric.nn import GATConv


# Config
SAPBERT_EMB_PATH = 'kg_sapbert_embeddings.npy'
EDGES_CSV_PATH   = 'kg_edges.csv'
NODES_CSV_PATH   = 'kg_nodes.csv'
OUTPUT_PATH      = 'kg_gat_embeddings.npy'

IN_DIM      = 768
HIDDEN_DIM  = 256
OUT_DIM     = 64
HEADS       = 4
DROPOUT     = 0.1
N_RELATIONS = 6


# Model
class KG_GAT(nn.Module):
    def __init__(self, in_dim=IN_DIM, hidden_dim=HIDDEN_DIM, out_dim=OUT_DIM,
                 heads=HEADS, dropout=DROPOUT, n_relations=N_RELATIONS):
        super().__init__()
        self.edge_type_emb = nn.Embedding(n_relations, in_dim)
        self.conv1  = GATConv(in_dim, hidden_dim // heads, heads=heads, dropout=dropout)
        self.conv2  = GATConv(hidden_dim, out_dim, heads=1, dropout=dropout)
        self.norm1  = nn.LayerNorm(hidden_dim)
        self.norm2  = nn.LayerNorm(out_dim)
        self.drop   = nn.Dropout(dropout)
        self.act    = nn.ELU()

    def forward(self, x, edge_index, edge_type):
        # Inject edge type signal into source node features
        edge_feat           = self.edge_type_emb(edge_type)       # (E, in_dim)
        x_mod               = x.clone()
        x_mod[edge_index[0]] = x[edge_index[0]] + edge_feat

        h = self.conv1(x_mod, edge_index)
        h = self.norm1(h)
        h = self.act(h)
        h = self.drop(h)
        h = self.conv2(h, edge_index)
        h = self.norm2(h)
        return h                                                    # (N, 64)


# Load inputs
print('Loading SapBERT embeddings...')
node_embeddings = np.load(SAPBERT_EMB_PATH)                        # (N, 768)
print(f'  node_embeddings: {node_embeddings.shape}')

print('Loading edges...')
edges_df = pd.read_csv(EDGES_CSV_PATH)
print(f'  edges: {len(edges_df)}')

# Validate no NaN indices
edges_df = edges_df.dropna(subset=['src_idx', 'dst_idx', 'rel_idx'])
edges_df[['src_idx', 'dst_idx', 'rel_idx']] = \
    edges_df[['src_idx', 'dst_idx', 'rel_idx']].astype(int)

# Validate index bounds
n_nodes = len(node_embeddings)
edges_df = edges_df[
    (edges_df['src_idx'] < n_nodes) &
    (edges_df['dst_idx'] < n_nodes)
]
print(f'  edges after validation: {len(edges_df)}')

# Build tensors
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Device: {device}')

x = torch.tensor(node_embeddings, dtype=torch.float32).to(device)

edge_index = torch.tensor(
    edges_df[['src_idx', 'dst_idx']].values.T,    # (2, E)
    dtype=torch.long
).to(device)

edge_type = torch.tensor(
    edges_df['rel_idx'].values,
    dtype=torch.long
).to(device)

print(f'x:          {x.shape}')
print(f'edge_index: {edge_index.shape}')
print(f'edge_type:  {edge_type.shape}')


# Run GAT
model = KG_GAT().to(device)
model.eval()

print('Running GAT...')
with torch.no_grad():
    kg_embeddings = model(x, edge_index, edge_type)   # (N, 64)

kg_embeddings = kg_embeddings.cpu().numpy().astype(np.float32)
print(f'Output shape: {kg_embeddings.shape}')


# Save
np.save(OUTPUT_PATH, kg_embeddings)
print(f'Saved → {OUTPUT_PATH}')


# Build lookup and sanity check
all_nodes  = pd.read_csv(NODES_CSV_PATH)
id_to_idx  = dict(zip(all_nodes['id'], all_nodes['node_idx']))

def lookup(node_id: str) -> np.ndarray:
    idx = id_to_idx.get(node_id)
    if idx is None:
        return np.zeros(OUT_DIM, dtype=np.float32)
    return kg_embeddings[idx]

# Spot check
sample_id   = all_nodes.iloc[0]['id']
sample_name = all_nodes.iloc[0]['name']
sample_emb  = lookup(sample_id)
print(f'\nSpot check — "{sample_name}" (id={sample_id}):')
print(f'  embedding shape: {sample_emb.shape}')
print(f'  embedding norm:  {np.linalg.norm(sample_emb):.4f}')
print(f'  value range:     [{sample_emb.min():.3f}, {sample_emb.max():.3f}]')