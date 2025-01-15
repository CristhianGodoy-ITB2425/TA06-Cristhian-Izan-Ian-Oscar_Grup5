import os

# Definir la cabecera correcta
correct_header = "precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1"

# Ruta de la carpeta
folder_path = "PRECIPITACIONS"

# Ruta del archivo de log de errores
error_log_path = "Error_log.log"

# Función para determinar el delimitador
def determinar_delimitador(linea):
    if ',' in linea:
        return ','
    elif '\t' in linea:
        return '\t'
    elif ' ' in linea:
        return ' '
    else:
        return None

# Función para comparar filas
def comparar_filas(fila1, fila2):
    return fila1 == fila2

# Abrir el archivo de log de errores en modo de escritura
with open(error_log_path, 'w') as error_log:
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
                    error_message = f"{filename}: Cabecera incorrecta\n"
                    print(error_message.strip())
                    error_log.write(error_message)

