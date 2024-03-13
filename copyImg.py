import os
from tkinter import filedialog
from tqdm import tqdm
import shutil

def select_directories():
    list_folders = []  
    path_root = filedialog.askdirectory(title='Seleccione el directorio raíz')
    while path_root:
        list_folders.append(path_root)
        path_root = filedialog.askdirectory(title='Seleccione otro directorio o cancele para continuar')
    if not list_folders:
        raise Exception("No se seleccionó ningún directorio")
    
    return list_folders


labelsPath = 'labels'

# Guarda en lista los archivoc en labelsPath
labels = os.listdir(labelsPath)

print("Seleccione carpeta de imagenes...")

list_folders = select_directories()
for path_root in list_folders:

    for folder_path in os.listdir(path_root):
        if folder_path.endswith('PP'):
            # Recorrer todos los archivos en la carpeta
            path = os.path.join(path_root, folder_path)
            
            for filename in tqdm(os.listdir(os.path.join(path,"cvat")),desc="Contando Imágenes"):
                # Contar la cantidad de imágenes
                if filename.split(".")[0] in labels:
                    # Construir la ruta completa al archivo
                    file_path = os.path.join(path, "cvat", filename)
                    shutil.copy(file_path, 'images')
                    