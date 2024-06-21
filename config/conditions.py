import json
import os
import importlib.util
import re



def charger_configuration(nom_fichier):
    with open(nom_fichier, 'r') as f:
        config = json.load(f)
    return config


configuration = charger_configuration('/molika/config/config.json')



def lire_synonymes():
    synonymes = {}
    chemin_synonymes = "/molika/config/simi.txt"
    if os.path.exists(chemin_synonymes):
        with open(chemin_synonymes, "r") as f:
            lignes = f.readlines()
            for ligne in lignes:
                mots = ligne.strip().split(",")
                mot_principal = mots[0]
                synonymes[mot_principal] = mots
    return synonymes

def check_conditions(phrase):
    try:
        synonymes = lire_synonymes()
        mots = phrase.lower().split()

        if any(syn in mots for syn in synonymes.get("bonjour", [])):
            return "Bonjour !"
        
        if any(syn in mots for syn in synonymes.get("au revoir", [])):
            return "Au revoir Monsieur"
        
        if all(any(syn in mots for syn in syn_list) for syn_list in synonymes.values() if syn_list[0] in ["crée", "nouveau", "projet"]):
            mots_commande = phrase.split() 
            dernier_mot = mots_commande[-1] 
            dossier_cree = os.path.join(configuration['repertoire_projet'], dernier_mot)
            try:
                os.makedirs(dossier_cree)  # Crée le nouveau dossier
                return f"Le dossier '{dernier_mot}' a été créé avec succès dans {dossier_cree}"
            except OSError as e:
                return f"Erreur lors de la création du dossier: {str(e)}"

        if any(syn in mots for syn in synonymes.get("allume", [])):
            try:
                chemin_script_wol = "/molika/script/WOL.py"
                spec = importlib.util.spec_from_file_location("wol", chemin_script_wol)
                wol = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(wol)
                resultat = wol.wake_on_lan(phrase)
                return resultat
            except FileNotFoundError:
                return("Le fichier WOL.py n'a pas été trouvé à l'emplacement {chemin_script_wol}.")        
        
        if all(any(syn in mots for syn in syn_list) for syn_list in synonymes.values() if syn_list[0] in ["quelles", "projet", "cour"]):
            if os.path.exists(configuration['repertoire_projet']):
                dossiers = [d for d in os.listdir(configuration['repertoire_projet']) if os.path.isdir(os.path.join(configuration['repertoire_projet'], d)) and not d.startswith("0_")]
                if dossiers:
                    liste_dossiers = ", ".join(dossiers)
                    return f"Voici les projets en cours : {liste_dossiers}."
                else:
                    return "Il n'y a aucun projet en cours."
            else:
                return "Le répertoire des projet n'existe pas."
        
        if all(any(syn in mots for syn in syn_list) for syn_list in synonymes.values() if syn_list[0] in ["lance", "archive", "projet"]):
            
            repertoire_projet = configuration['repertoire_projet']
            dossiers = os.listdir(repertoire_projet)

            # Identification du mot correspondant au nom d'un dossier
            mot_identifie = None
            mots_lower = [mot.lower() for mot in mots]
            for mot in dossiers:
                if mot.lower() in mots_lower:
                    mot_identifie = mot
                    break

            if mot_identifie:
                chemin_dossier = os.path.join(repertoire_projet, mot_identifie)
                repertoire_archive = configuration['repertoire_archive']
                chemin_archive = os.path.join(repertoire_archive, mot_identifie)
                os.rename(chemin_dossier, chemin_archive)
                return f"Le projet '{mot_identifie}' a été déplacé vers le répertoire d'archivage."
            else:
                return "je n'ai pas trouvé de quelle projet vous parlez."
        
        
        
        return "Que puis-je faire pour vous ?"
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

