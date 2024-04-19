#!/bin/bash

config_file="/molika/config/config.json"


if [ ! -e "$config_file" ]; then
    echo "Le fichier config.json n'existe pas. Création du fichier avec les valeurs par défaut."

    config_content='{
    "repertoire_projet": "/molika/log/",
    "WOL1": "TA:DA:AA:AA,AU:TR:EE:MA:CA:DR:ES:SS",
    "WOL2": "TA:DA:AA:AA"
}
'
    echo "$config_content" > "$config_file"
    
    echo "Le fichier config.json a été créé avec succès."
else
    echo "Le fichier config.json existe déjà."
fi



if [ -e "/molika/config/conditions.py" ]; then
    echo "Le fichier conditions.py existe dans /molika/config/. Suppression du fichier dans /molika/."
    rm /molika/conditions.py
else
    echo "Le fichier conditions.py n'existe pas dans /molika/config/. Déplacement de /molika/conditions.py vers /molika/config/conditions.py."
    mv /molika/conditions.py /molika/config/conditions.py
    echo "Le fichier conditions.py a été déplacé avec succès vers /molika/config/."
fi

if [ -e "/molika/config/simi.txt" ]; then
    echo "Le fichier simi.txt existe dans /molika/config/. Suppression du fichier dans /molika/."
    rm /molika/simi.txt
else
    echo "Le fichier simi.txt n'existe pas dans /molika/config/. Déplacement de /molika/simi.txt vers /molika/config/simi.txt."
    mv /molika/simi.txt /molika/config/simi.txt
    echo "Le fichier simi.txt a été déplacé avec succès vers /molika/config/."
fi

if [ -e "/molika/config/task.csv" ]; then
    echo "Le fichier task.csv existe dans /molika/config/. Suppression du fichier dans /molika/."
    rm /molika/task.csv
else
    echo "Le fichier task.csv n'existe pas dans /molika/config/. Déplacement de /molika/task.csv vers /molika/config/task.csv."
    mv /molika/task.csv /molika/config/task.csv
    echo "Le fichier task.csv a été déplacé avec succès vers /molika/config/."
fi

