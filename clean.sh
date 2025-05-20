#!/bin/bash

find . -type d -name "__pycache__" -exec rm -r {} +
rm ./model/gnn_weights.pth
rm graph.gpickle
rm -r ./lib
rm graph.html
rm ./data/nodes_updated.csv

if [ $? -eq 0 ]; then
    clear
    echo "Succès du nettoyage."
else
    echo "Une erreur est survenue pendant le nettoyage."
fi
