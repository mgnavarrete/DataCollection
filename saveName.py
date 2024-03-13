import os
from tkinter import filedialog
from tqdm import tqdm
import pandas as pd


def select_directories():
    list_folders = []  
    path_root = filedialog.askdirectory(title='Seleccione el directorio raíz')
    while path_root:
        list_folders.append(path_root)
        path_root = filedialog.askdirectory(title='Seleccione otro directorio o cancele para continuar')
    if not list_folders:
        raise Exception("No se seleccionó ningún directorio")
    
    return list_folders
    
class_counts = [0] * 9 

print("Seleccione carpetas de fallas...")
list_folders = select_directories()
labeled_images = 0
for folder_path in list_folders:
    
    # Recorrer todos los archivos en la carpeta
    for filename in tqdm(os.listdir(folder_path),desc="Contando fallas en carpeta" + folder_path):
        if filename.endswith('.txt'):
            # Construir la ruta completa al archivo
            file_path = os.path.join(folder_path, filename)
            
            # Abrir y leer el archivo
            with open(file_path, 'r') as file:
                added = False
                for line in file:
                    if line != "\n" or line != "":
                        if not added:
                            #Guardar el nombre del archivo sin la extensión en un archivo
                            with open("saveName.csv", "a") as file:
                                file.write(filename.split(".")[0] + ",\n")
                            labeled_images += 1
                            added = True
                    # Extraer la clase de la detección
                    class_id = int(line.split()[0])
                    
                    # Incrementar el contador para esa clase
                    class_counts[class_id] += 1

    # Calcular la cantidad total de fallas
    total_fallas = sum(class_counts)
