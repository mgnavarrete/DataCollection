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
    
    if f"{pc}-{ubicacion}" not in ubicaciones:
        ubicaciones.append(f"{pc}-{ubicacion}")
    
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
                            labeled_images += 1
                            added = True
                    # Extraer la clase de la detección
                    class_id = int(line.split()[0])
                    
                    # Incrementar el contador para esa clase
                    class_counts[class_id] += 1

    # Calcular la cantidad total de fallas
    total_fallas = sum(class_counts)

# Guardar los resultados en un archivo cvs
output_file = "dataCollection.csv"
tipo_fallas = ["StringDesconectado", "StringCortoCircuito", "ModuloCircuitoAbierto", "BusBar", "ModuloCortoCircuito", "CelulaCaliente", "ByPass", "PID", "Tracker Fuera de Pos"]
if not os.path.exists(output_file):
    # crear DF con pandas con las columnas necesarias
    dataFile = pd.DataFrame(columns=['Planta',
                                     'Fecha Levantamiento', 
                                     'Ubicacion', 
                                     'Total Imagenes', 
                                     'Imagenes Etiquetadas', 
                                     'Total de fallas', 
                                     'StringDesconectado', 
                                     'StringCortoCircuito', 
                                     'ModuloCircuitoAbierto',
                                     'BusBar', 
                                     'ModuloCortoCircuito', 
                                     'CelulaCaliente', 
                                     'ByPass', 
                                     'PID', 
                                     'Tracker Fuera de Pos'
                                 ])  
else: 
    # crear data con pandas
    dataFile = pd.read_csv(output_file)
    
image_counts = 0

print("Seleccione carpeta de imagenes...")

list_folders = select_directories()
for path_root in list_folders:
    ubicacion = path_root.split(":")[0]
    
    if f"{pc}-{ubicacion}" not in ubicaciones:
        ubicaciones.append(f"{pc}-{ubicacion}")
    # Recorrer solo las carpetas que terminan en PP
    for folder_path in os.listdir(path_root):
        if folder_path.endswith('PP'):
            # Recorrer todos los archivos en la carpeta
            path = os.path.join(path_root, folder_path)
            
            for filename in tqdm(os.listdir(os.path.join(path,"Temp")),desc="Contando Imágenes"):
                # Contar la cantidad de imágenes
                image_counts += 1


# Puede que hayan filas con mismo nombre pero distinta fecha
if ((dataFile['Planta'] == planta) & (dataFile['Fecha Levantamiento'] == date)).any():

    print("Ya existe una fila con el mismo nombre de planta y fecha")
    
    # sumar valor antiguo con nuevo para los valore con el mismo nombre de planta y misma fecha\    
    dataFile.loc[(dataFile['Planta'] == planta) & (dataFile['Fecha Levantamiento'] == date), 'Imagenes Etiquetadas'] += labeled_images
    
    dataFile.loc[(dataFile['Planta'] == planta) & (dataFile['Fecha Levantamiento'] == date), 'Total de fallas'] += total_fallas
    
    for i, falla in enumerate(tipo_fallas):
        dataFile.loc[(dataFile['Planta'] == planta) & (dataFile['Fecha Levantamiento'] == date), falla] += class_counts[i]
        
    
    # Agregar nuevas ubicaciones
    dataFile.loc[(dataFile['Planta'] == planta) & (dataFile['Fecha Levantamiento'] == date), 'Ubicacion'] = ", ".join(ubicaciones)
    
    dataFile.loc[(dataFile['Planta'] == planta) & (dataFile['Fecha Levantamiento'] == date), 'Total Imágenes'] += image_counts
    
else:
    # Agregar nueva fila usando concat
    dataFile = pd.concat([dataFile, pd.DataFrame({
    'Planta': [planta], 
    'Fecha Levantamiento': [date],
    'Ubicacion': [", ".join(ubicaciones)],
    'Total Imagenes': [image_counts],
    'Imagenes Etiquetadas': [labeled_images],
    'Total de fallas': [total_fallas], 
    'StringDesconectado': [class_counts[0]],
    'StringCortoCircuito': [class_counts[1]],
    'ModuloCircuitoAbierto': [class_counts[2]],
    'BusBar': [class_counts[3]],
    'ModuloCortoCircuito': [class_counts[4]],
    'CelulaCaliente': [class_counts[5]],
    'ByPass': [class_counts[6]],
    'PID': [class_counts[7]],
    'Tracker Fuera de Pos': [class_counts[8]]
})])
 
# Guardar el archivo
dataFile.to_csv(output_file, index=False)
print(f"Archivo guardado en {output_file}")
