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
    
print("Ingrese computador:")
pc = input()
    
print("Ingrese fecha de levantamiento:")
date = input()

print("Ingrese nombre de planta:")
planta = input()
class_counts = [0] * 9 

print("Seleccione carpetas de fallas...")
ubicaciones = []
list_folders = select_directories()
labeled_images = 0
for folder_path in list_folders:
    # Enontrar nombre del disco duro donde se encuentra la carpeta
    ubicacion = folder_path.split(":")[0]
    
    if f"{pc}-{ubicacion}" not in ubicacion:
        ubicaciones.append(f"{pc}-{ubicacion}")
    
    # Recorrer todos los archivos en la carpeta
    for filename in tqdm(os.listdir(folder_path),desc="Contando fallas en carpeta" + folder_path):
        if filename.endswith('.txt'):
            # Construir la ruta completa al archivo
            file_path = os.path.join(folder_path, filename)
            
            # Abrir y leer el archivo
            with open(file_path, 'r') as file:
                # si el archivo tiene texto sumar 1 a la cantidad de imagenes etiquetadas
                if file.read(1):
                    labeled_images += 1
                for line in file:    
                    # Extraer la clase de la detección
                    class_id = int(line.split()[0])
                    
                    # Incrementar el contador para esa clase
                    class_counts[class_id] += 1

    # Calcular la cantidad total de fallas
    total_fallas = sum(class_counts)

# Imprimir los resultados
print(f"Total de imágenes etiquetadas: {labeled_images}")
print(f"Total de fallas: {total_fallas}")
for i, count in enumerate(class_counts):
    print(f"Clase {i}: {count}")

# Guardar los resultados en un archivo cvs
output_file = "dataCollection.csv"

if not os.path.exists(output_file):
    # crear DF con pandas con las columnas necesarias
    dataFile = pd.DataFrame(columns=['Planta', 
                                 'Ubicacion', 
                                 'Total Imagenes', 
                                 'Imagenes Etiquetadas', 
                                 'Total de fallas', 
                                 'Clase 0', 
                                 'Clase 1', 
                                 'Clase 2', 
                                 'Clase 3', 
                                 'Clase 4', 
                                 'Clase 5', 
                                 'Clase 6', 
                                 'Clase 7', 
                                 'Clase 8'])  



if f"{planta}-{date}" in dataFile['Planta'].values:
    # sumar valor antiguo con nuevo
    dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", 'Imagenes Etiquetadas'] += labeled_images
    
    dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", 'Total de fallas'] += total_fallas
    for i in range(9):
        dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", f'Clase {i}'] += class_counts[i]
    
    # Agregar nuevas ubicaciones
    dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", 'Ubicacion'] = ", ".join(ubicaciones)

    
else:
    # Agregar nueva fila usando concat
    dataFile = pd.concat([dataFile, pd.DataFrame({
    'Planta': [f"{planta}-{date}"], 
    'Ubicacion': [", ".join(ubicaciones)],
    'Total Imagenes': [0],
    'Imagenes Etiquetadas': [labeled_images],
    'Total de fallas': [total_fallas], 
    'Clase 0': [class_counts[0]],
    'Clase 1': [class_counts[1]],
    'Clase 2': [class_counts[2]],
    'Clase 3': [class_counts[3]],
    'Clase 4': [class_counts[4]],
    'Clase 5': [class_counts[5]],
    'Clase 6': [class_counts[6]],
    'Clase 7': [class_counts[7]],
    'Clase 8': [class_counts[8]]
})], ignore_index=True)
 
    
# Guardar el archivo
dataFile.to_csv(output_file)
print(f"Archivo guardado en {output_file}")
