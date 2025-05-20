# init_house.py
import pandas as pd

def infer_house(name: str) -> str:
    name = name.lower()
    if "stark" in name:
        return "Stark"
    elif "lannister" in name:
        return "Lannister"
    elif "baratheon" in name:
        return "Baratheon"
    elif "targaryen" in name:
        return "Targaryen"
    elif "greyjoy" in name:
        return "Greyjoy"
    elif "tyrell" in name:
        return "Tyrell"
    elif "martell" in name:
        return "Martell"
    elif "tully" in name:
        return "Tully"
    elif "arryn" in name:
        return "Arryn"
    elif "frey" in name:
        return "Frey"
    elif "bolton" in name:
        return "Bolton"
    elif "clegane" in name:
        return "Clegane"
    elif "mormont" in name:
        return "Mormont"
    elif "baelish" in name:
        return "Baelish"
    elif "seaworth" in name:
        return "Seaworth"
    elif "sand" in name:
        return "Martell"
    elif "snow" in name:
        return "Stark"
    elif "pycelle" in name:
        return "Lannister"
    elif "melisandre" in name:
        return "Baratheon"
    else:
        return "Unknown"


nodes = pd.read_csv("data/nodes.csv")

nodes['House'] = nodes['Label'].apply(infer_house)
nodes.to_csv("data/nodes.csv", index=False)

print("Task Done")
