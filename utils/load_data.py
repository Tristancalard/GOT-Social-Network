# utils/load_data.py
import torch
import pandas as pd
import networkx as nx
from torch_geometric.data import Data


def load_data():
    nodes = pd.read_csv("data/nodes.csv")
    edges = pd.read_csv("data/edges.csv")
    return nodes, edges


def build_graph(nodes: pd.DataFrame, edges: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    for _, row in nodes.iterrows():
        G.add_node(row['Id'], label=row['Label'], house=row['House'])
    for _, row in edges.iterrows():
        G.add_edge(row['Source'], row['Target'], weight=row['weight'], type=row['Type'])
    return G


def graph_to_data(G: nx.Graph, nodes: pd.DataFrame) -> Data:
    id_to_idx = {nid: idx for idx, nid in enumerate(nodes['Id'])}

    edges_idx = []
    for u, v in G.edges():
        edges_idx.append([id_to_idx[u], id_to_idx[v]])
        edges_idx.append([id_to_idx[v], id_to_idx[u]])
    edge_index = torch.tensor(edges_idx, dtype=torch.long).t().contiguous()

    house_list = nodes['House'].unique().tolist()
    house_to_idx = {h: i for i, h in enumerate(house_list)}
    x = torch.zeros((len(nodes), len(house_list)), dtype=torch.float)
    for i, h in enumerate(nodes['House']):
        x[i, house_to_idx[h]] = 1.0

    y = torch.tensor([house_to_idx[h] for h in nodes['House']], dtype=torch.long)

    return Data(x=x, edge_index=edge_index, y=y)
