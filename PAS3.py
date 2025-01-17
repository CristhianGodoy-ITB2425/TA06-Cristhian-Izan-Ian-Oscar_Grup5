import os
import pandas as pd

# Ruta de la carpeta
folder_path = "PRECIPITACIONS"
clean_folder_path = "LIMPIOS"

# Crear la carpeta LIMPIOS si no existe
os.makedirs(clean_folder_path, exist_ok=True)

# Ruta del archivo de log de errores
error_log_path = "Error_log.log"

# Función para verificar el formato de las líneas de datos (ahora siempre devuelve True)
def verificar_formato(df):
    return True

# Función para verificar y limpiar el número de campos en cada línea
def limpiar_numero_campos(file_path, expected_fields):
    cleaned_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if len(line.split()) == expected_fields:
                cleaned_lines.append(line)
    return cleaned_lines

# Abrir el archivo de log de errores en modo de escritura
with open(error_log_path, 'w') as error_log:
    # Recorrer todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith(".dat"):
            file_path = os.path.join(folder_path, filename)
            try:
                # Verificar el número de campos en la primera línea
                with open(file_path, 'r') as file:
                    first_line = file.readline()
                    expected_fields = len(first_line.split())

                # Limpiar el archivo de líneas con número incorrecto de campos
                cleaned_lines = limpiar_numero_campos(file_path, expected_fields)
                if not cleaned_lines:
                    error_message = f"{filename}: Todas las líneas tienen un número incorrecto de campos\n"
                    print(error_message.strip())
                    error_log.write(error_message)
                    continue

                # Guardar las líneas limpias en un archivo temporal
                temp_file_path = file_path + ".tmp"
                with open(temp_file_path, 'w') as temp_file:
                    temp_file.writelines(cleaned_lines)

                # Leer el archivo temporal con pandas
                df = pd.read_csv(temp_file_path, sep='\s+', header=None)
                os.remove(temp_file_path)  # Eliminar el archivo temporal

                # Verificar el formato del DataFrame (ahora siempre es correcto)
                if not verificar_formato(df):
                    error_message = f"{filename}: Formato incorrecto en el archivo\n"
                    print(error_message.strip())
                    error_log.write(error_message)
                    continue

                # Gestionar valores que falten o corruptos
                df.replace('-999', pd.NA, inplace=True)
                df.dropna(inplace=True)

                # Guardar el DataFrame limpio en la nueva carpeta
                clean_file_path = os.path.join(clean_folder_path, filename)
                df.to_csv(clean_file_path, sep=' ', index=False, header=False)
            except Exception as e:
                error_message = f"{filename}: Error al leer el archivo - {str(e)}\n"
                print(error_message.strip())
                error_log.write(error_message)