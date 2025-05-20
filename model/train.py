# model/train.py
import torch
import torch.nn.functional as F
from utils.load_data import load_data, build_graph, graph_to_data
from model.gcn import GCN
import pickle

# Chargement
nodes, edges = load_data()
G = build_graph(nodes, edges)
data = graph_to_data(G, nodes)

# Masque d'entraînement (exclude Unknown)
train_mask = nodes['House'] != 'Unknown'

# Modèle et optimizer
model = GCN(
    in_channels=data.num_node_features,
    hidden_channels=64,
    out_channels=int(data.y.max().item() + 1)
)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Entraînement
model.train()
for epoch in range(1, 201):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[train_mask], data.y[train_mask])
    loss.backward()
    optimizer.step()
    if epoch % 20 == 0:
        pred = out.argmax(dim=1)
        acc = (pred[train_mask] == data.y[train_mask]).sum().item() / train_mask.sum()
        print(f"Epoch {epoch:03d} | Loss: {loss:.4f} | Acc: {acc:.4f}")

# Sauvegarde des poids
torch.save(model.state_dict(), './model/gnn_weights.pth')

# Prédiction des Unknown puis mise à jour
model.eval()
with torch.no_grad():
    out = model(data)
    preds = out.argmax(dim=1).cpu().numpy()

house_list = nodes['House'].unique().tolist()
# Remplacer les Unknown
nodes.loc[nodes['House']=='Unknown', 'House'] = [
    house_list[p] for p in preds[nodes['House']=='Unknown']
]

# Rebuild et sauvegarde du graphe mis à jour
G = build_graph(nodes, edges)
with open('./graph.gpickle', 'wb') as f:
    pickle.dump(G, f)
print("Maisons prédites et graphe mis à jour.")

# Facultatif : sauvegarder le CSV mis à jour
nodes.to_csv('data/nodes_updated.csv', index=False)
