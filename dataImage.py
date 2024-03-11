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
    
    
print("Ingrese fecha de levantamiento:")
date = input()

print("Ingrese nombre de planta:")
planta = input()
image_counts = 0

print("Seleccione carpeta de imagenes...")

path_root = filedialog.askdirectory(title='Seleccione el directorio raíz')

# Recorrer solo las carpetas que terminan en PP
for folder_path in os.listdir(path_root):
    if folder_path.endswith('PP'):
        # Recorrer todos los archivos en la carpeta
        path = os.path.join(path_root, folder_path)
        
        for filename in tqdm(os.listdir(os.path.join(path,"Temp")),desc="Contando Imágenes"):
            # Contar la cantidad de imágenes
            image_counts += 1

# Imprimir los resultados
print(f"Total de imagenes: {image_counts}")

# Guardar los resultados en un archivo cvs
output_file = "dataCollection.csv"

# crear data con pandas
dataFile = pd.read_csv(output_file, encoding='ISO-8859-1')

if f"{planta}-{date}" in dataFile['Planta'].values:
    # Actualizar la fila existente
    dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", 'Total Imágenes'] += image_counts

    
# Guardar el archivo
dataFile.to_csv(output_file, index=False, encoding='ISO-8859-1')
print(f"Archivo guardado en {output_file}")