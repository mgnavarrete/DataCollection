import os
from tkinter import filedialog

print("Ingrese fecha de levantamiento:")
date = input()

print("Ingrese nombre de planta:")
planta = input()
class_counts = [0] * 9 
while True:
    print("Seleccione carpeta de fallas...")
    folder_path = filedialog.askdirectory(title='seleccione carpeta de fallas')

    if folder_path is None:
        break

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
        file.write("Fecha de levantamiento,Planta,Total de fallas,")
        for i in range(9):
            file.write(f"Clase {i},")
        file.write("\n")
else:
    with open(output_file, 'a') as file:
        file.write(f"{date},{planta},{total_fallas},")
        for count in class_counts:
            file.write(f"{count},")
        file.write("\n")