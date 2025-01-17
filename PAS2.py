import os

# Ruta de la carpeta
folder_path = "PRECIPITACIONS"

# Ruta del archivo de log de errores
error_log_path = "Error_log.log"


# Función para verificar el formato de las líneas de datos
def verificar_formato(linea):
    partes = linea.split()
    if len(partes) < 3:
        return False
    estacion = partes[0]
    año = partes[1]
    datos = partes[2:]

    if not estacion.startswith("P") or not estacion[1:].isdigit():
        return False
    if not año.isdigit() or len(año) != 4:
        return False
    for dato in datos:
        if dato != "-999" and not dato.isdigit():
            return False
    return True


# Abrir el archivo de log de errores en modo de escritura
with open(error_log_path, 'w') as error_log:
    # Recorrer todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith(".dat"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                # Leer todas las líneas del archivo
                lineas = file.readlines()
                # Verificar las líneas a partir de la tercera
                for i, linea in enumerate(lineas[2:], start=3):
                    if not verificar_formato(linea.strip()):
                        error_message = f"{filename}: Formato incorrecto en la línea {i}\n"
                        print(error_message.strip())
                        error_log.write(error_message)
                        break