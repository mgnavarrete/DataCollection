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
        
        for filename in tqdm(os.listdir(os.path.join(path,"original_img")),desc="Contando Imágenes"):
            # Contar la cantidad de imágenes
            image_counts += 1

# Imprimir los resultados
print(f"Total de imagenes: {image_counts}")

# Guardar los resultados en un archivo cvs
output_file = "dataCollection.csv"
# crear dataFrame con pandas
if not os.path.exists(output_file):
    with open(output_file, 'w') as file:
        file.write("Planta,Ubicación,Total Imágenes,Imagenes Etiquetadas,Total de fallas,")
        for i in range(9):
            file.write(f"Clase {i},")
        file.write("\n")
    

# crear data con pandas
dataFile = pd.read_csv(output_file, encoding='ISO-8859-1')

if f"{planta}-{date}" in dataFile['Planta'].values:
    # Actualizar la fila existente
    dataFile.loc[dataFile['Planta'] == f"{planta}-{date}", 'Total Imágenes'] = image_counts

    
else:
    # Agregar nueva fila y dejar columnas como no definido
    dataFile = dataFile.append({'Planta': f"{planta}-{date}", 
                                'Ubicación': 'No definido', 
                                'Total Imágenes': image_counts, 
                                'Imagenes Etiquetadas': 'No definido', 
                                'Total de fallas': 'No definido',
                                'Clase 0': 'No definido',
                                'Clase 1': 'No definido',
                                'Clase 2': 'No definido',
                                'Clase 3': 'No definido',
                                'Clase 4': 'No definido',
                                'Clase 5': 'No definido',
                                'Clase 6': 'No definido',
                                'Clase 7': 'No definido',
                                'Clase 8': 'No definido'
                                
                                }, ignore_index=True)
    
# Guardar el archivo
dataFile.to_csv(output_file, index=False, encoding='ISO-8859-1')
print(f"Archivo guardado en {output_file}")