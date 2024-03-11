import os
from tkinter import filedialog

print("Seleccione carpeta de fallas...")

folder_path = filedialog.askdirectory(title='seleccione carpeta de fallas')


# Contadores para cada clase inicializados en cero
class_counts = [0] * 9  # Asumiendo que las clases van de 0 a 8

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
