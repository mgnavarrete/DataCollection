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
class_counts = [0] * 9 

print("Seleccione carpeta de imagenes...")

list_folders = select_directories()
for folder_path in tqdm(list_folders,  desc="Contando imágenes"):
    # Recorrer todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            # Construir la ruta completa al archivo
            file_path = os.path.join(folder_path, filename)
            
            # Abrir y leer el archivo
            with open(file_path, 'r') as file:
                for line in file:
                    # Extraer la clase de la detección
                    class_id = int(line.split()[0])
                    
                    # Incrementar el contador para esa clase
                    class_counts[class_id] += 1

    # Calcular la cantidad total de fallas
    total_fallas = sum(class_counts)

# Imprimir los resultados
print(f"Total de fallas: {total_fallas}")
for i, count in enumerate(class_counts):
    print(f"Clase {i}: {count}")

# Guardar los resultados en un archivo cvs
output_file = "dataColecction.csv"
# Si no existe el archivo, crearlo
if not os.path.exists(output_file):
    with open(output_file, 'w') as file:
        file.write("Planta,Ubicación,Total Imágenes,Imagenes Etiquetadas,Total de fallas,")
        for i in range(9):
            file.write(f"Clase {i},")
        file.write("\n")

# crear data con pandas
dataFile = pd.read_csv(output_file)
if f"{planta}-{date}" in dataFile['Planta'].values:
    # Actualizar la fila existente
    dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", 'Total de fallas'] = total_fallas
    for i in range(9):
        dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", f'Clase {i}'] = class_counts[i]
else:
    # Agregar nueva fila y dejar columnas vacias
    
    dataFile = dataFile.append({
        'Planta': f"{planta}-{date}", 
        'Ubicación': "No definida",
        'Total Imágenes': "No definida",
        'Imagenes Etiquetadas': "No definida",
        'Total de fallas': total_fallas, 
        'Clase 0': class_counts[0],
        'Clase 1': class_counts[1],
        'Clase 2': class_counts[2],
        'Clase 3': class_counts[3],
        'Clase 4': class_counts[4],
        'Clase 5': class_counts[5],
        'Clase 6': class_counts[6],
        'Clase 7': class_counts[7],
        'Clase 8': class_counts[8]
    }, ignore_index=True)