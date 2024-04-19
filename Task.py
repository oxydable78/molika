import csv
from datetime import datetime, timedelta
import time
import os
import importlib.util

# Fonction pour charger les tâches à partir du fichier CSV
def load_tasks(file_path):
    tasks = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                tasks.append(row)
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'existe pas.")
    return tasks

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
        
   
def exporter_journal(date, date_file, user, input_commande, output):
    chemin_journal = f"/molika/log/{date}_molika.csv"
    existe_deja = os.path.isfile(chemin_journal)

    with open(chemin_journal, mode='a', newline='') as fichier_csv:
        fieldnames = ['Date', 'Utilisateur', 'Commande_Input', 'Output']
        writer = csv.DictWriter(fichier_csv, fieldnames=fieldnames, delimiter=';')  # Spécifier le délimiteur
        
        if not existe_deja:
            writer.writeheader()

        writer.writerow({'Date': date_file, 'Utilisateur': user, 'Commande_Input': input_commande, 'Output': output})
        
        
def supprimer_ligne(file_path, task_info):
    try:
        tasks = load_tasks(file_path)
        updated_tasks = [task for task in tasks if not all(task[key] == task_info[key] for key in task_info)]
        with open(file_path, 'w', newline='') as file:
            fieldnames = tasks[0].keys() if tasks else []
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(updated_tasks)
        
        print("La ligne correspondant à la tâche spécifiée a été supprimée avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la suppression de la ligne : {str(e)}")



def process_tasks(tasks, file_path):
    if tasks:
        current_date = datetime.now()
        for task in tasks:
            end_date = datetime.strptime(task['fin'], "%d-%m-%Y")
            start_date = datetime.strptime(task['date'], "%d-%m-%Y")
            if end_date < current_date:
                supprimer_ligne(file_path, task)
                print("tada")
            elif start_date < current_date < end_date:
                task_time = datetime.strptime(task['heur'], "%H:%M").time()
                task_time_minus_15 = (datetime.combine(datetime.min, task_time) - timedelta(minutes=15)).time()
                print("tada2")
                if task_time and task_time < datetime.now().time() and task_time >= task_time_minus_15:
                    resultat = executer_conditions(task['heur'])
                    print("tada3")
                    if resultat:
                        date = datetime.now().strftime("%Y-%m-%d")
                        date_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        user = "planif"
                        texte = task['task']
                        exporter_journal(date, date_file, user, texte, resultat)
                        supprimer_ligne(file_path, task)
                        

csv_file = '/molika/config/task.csv'

# Boucle principale
while True:
    current_minute = time.localtime().tm_min
    if current_minute % 15 == 0:
        tasks = load_tasks(csv_file)
        process_tasks(tasks, csv_file)
    time.sleep(120)
