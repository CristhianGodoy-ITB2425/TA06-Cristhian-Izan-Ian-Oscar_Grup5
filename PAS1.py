import os

# Definir la cabecera correcta
correct_header = "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1"

# Ruta de la carpeta
folder_path = "PRECIPITACIONS"

# Recorrer todos los archivos en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith(".dat"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            # Leer la primera línea
            first_line = file.readline().strip()
            # Verificar si la cabecera es correcta
            if first_line == correct_header:
                print(f"{filename}: Cabecera correcta")
            else:
                print(f"{filename}: Cabecera incorrecta")
