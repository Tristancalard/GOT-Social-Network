# app/main.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pickle
import streamlit as st
import networkx as nx
from pyvis.network import Network

# Couleurs par maison
house_colors = {
    "Stark": "#1f77b4",
    "Lannister": "#d62728",
    "Baratheon": "#ff7f0e",
    "Targaryen": "#9467bd",
    "Greyjoy": "#bcbd22",
    "Tyrell": "#2ca02c",
    "Martell": "#e377c2",
    "Tully": "#8c564b",
    "Arryn": "#17becf",
    "Bolton": "#7f7f7f",
    "Frey": "#aec7e8",
    "Mormont": "#ffbb78",
    "Clegane": "#c5b0d5",
    "Baelish": "#98df8a",
    "Seaworth": "#ff9896",
    "Unknown": "#cccccc"
}

# Légende des maisons
st.sidebar.markdown("### Légende des Maisons")
for house, color in house_colors.items():
    st.sidebar.markdown(
        f"<span style='display:inline-block; width:12px; height:12px; background:{color}; margin-right:4px;'></span> {house}",
        unsafe_allow_html=True
    )

# Charger le graphe mis à jour
with open('graph.gpickle', 'rb') as f:
    G = pickle.load(f)

# Calcul d'un layout fixe
pos = nx.spring_layout(G, k=0.3, iterations=50)

# Titre
st.title("GOT Graph Viewer")

st.markdown("""
    <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }

        .css-18e3th9 {
            padding-top: 1rem !important;
        }

        .st-emotion-cache-1w723zb {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Disposition en deux colonnes : gauche = graphe, droite = infos
col1, col2 = st.columns([3, 1])

# Colonne de droite : panneau d'informations + recherche
with col2:
    labels = [attrs['label'] for _, attrs in G.nodes(data=True)]
    selected_label = st.selectbox("Choisir un personnage", sorted(labels))
    selected_id = next(
        n for n, attrs in G.nodes(data=True)
        if attrs['label'] == selected_label
    )
    attrs = G.nodes[selected_id]

    st.markdown(f"### {attrs['label']}")
    st.markdown(f"- **Maison :** {attrs.get('house', 'Unknown')}")

    neighbors = [
        (nbr, G.edges[selected_id, nbr]['weight'])
        for nbr in G.neighbors(selected_id)
    ]
    neighbors.sort(key=lambda x: -x[1])

    st.markdown("**Relations :**")

    relations_html = """
    <div style='max-height: 450px; overflow-y: auto; padding-left:10px; border:1px solid #ccc; border-radius:4px; padding:5px;'>
    """
    for nbr, w in neighbors:
        relations_html += f"<div>- {G.nodes[nbr]['label']} (poids : {w})</div>"
    relations_html += "</div>"

    st.markdown(relations_html, unsafe_allow_html=True)


# Colonne de gauche : visualisation du graphe + recherche zoom
with col1:
    nt = Network("800px", "100%", notebook=False)
    for n, attrs in G.nodes(data=True):
        x, y = pos[n]
        nt.add_node(
            n,
            label=attrs.get('label', n),
            title=f"Maison: {attrs.get('house','Unknown')}",
            color=house_colors.get(attrs.get('house','Unknown'), '#cccccc'),
            x=x * 1000,
            y=y * 1000,
            size=15
        )
    for u, v, attrs in G.edges(data=True):
        nt.add_edge(u, v, value=attrs['weight'])

    nt.set_options("""
    {
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 400,
          "springConstant": 0.05
        },
        "timestep": 0.5,
        "stabilization": {
          "enabled": true,
          "iterations": 30,
          "updateInterval": 5
        }
      }
    }
    """)
    nt.save_graph('graph.html')
    html = open('graph.html', 'r', encoding='utf-8').read()

    # Injection du champ de recherche et du script de zoom
    injected = html.replace(
        "<body>",
        """
        <body>
        <div style="padding:10px; text-align:center;">
          <input id="search" placeholder="🔍 Rechercher un personnage..."
                 style="width:300px; padding:5px; font-size:14px;"/>
        </div>
        """
    ).replace(
        "</body>",
        """
        <script type="text/javascript">
          const wait = setInterval(() => {
            if (window.network) {
              clearInterval(wait);
              // recherche et zoom
              document.getElementById('search').addEventListener('input', e => {
                const term = e.target.value.toLowerCase();
                const nodes = network.body.data.nodes.get();
                const match = nodes.find(n => n.label.toLowerCase().includes(term));
                if (match) {
                  network.focus(match.id, { scale: 1.2, animation: { duration: 300 } });
                  network.body.data.nodes.update({ id: match.id, borderWidth: 5 });
                }
              });
            }
          }, 100);
        </script>
        </body>
        """
    )
    st.components.v1.html(injected, height=650, scrolling=True)
