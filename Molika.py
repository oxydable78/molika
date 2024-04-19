import os
import importlib.util
import csv
from datetime import datetime
import sys


def lire_texte():
    if len(sys.argv) > 1:  
        texte = sys.argv[1]
    return texte
    

### lancement dans les condition
def executer_conditions(texte):
    try:
        chemin_conditions = "/molika/config/conditions.py"
        spec = importlib.util.spec_from_file_location("conditions", chemin_conditions)
        conditions = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conditions)
        resultat = conditions.check_conditions(texte)
        return resultat
    except FileNotFoundError:
        print("Le fichier conditions.py n'a pas été trouvé à l'emplacement spécifié.")
    except AttributeError:
        print("Le fichier conditions.py ne contient pas la fonction 'check_conditions'.")
      
### création d'une log  
def exporter_journal(date, date_file, user, input_commande, output):
    chemin_journal = f"/molika/log/{date}_molika.csv"
    existe_deja = os.path.isfile(chemin_journal)

    with open(chemin_journal, mode='a', newline='') as fichier_csv:
        fieldnames = ['Date', 'Utilisateur', 'Commande_Input', 'Output']
        writer = csv.DictWriter(fichier_csv, fieldnames=fieldnames, delimiter=';')  # Spécifier le délimiteur
        
        if not existe_deja:
            writer.writeheader()

        writer.writerow({'Date': date_file, 'Utilisateur': user, 'Commande_Input': input_commande, 'Output': output})




### lancement général
def main():
    user = os.environ.get('USER')
    texte = lire_texte()
    resultat = executer_conditions(texte) 
    if resultat:
        print("Molika :", resultat)
        date = datetime.now().strftime("%Y-%m-%d")
        date_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        exporter_journal(date, date_file, user, texte, resultat)
        

if __name__ == "__main__":
    main()
