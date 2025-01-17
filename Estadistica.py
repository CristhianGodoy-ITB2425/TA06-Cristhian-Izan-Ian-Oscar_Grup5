import os
import numpy as np

# Ruta de la carpeta
folder_path = "./PRECIPITACIONS"

# Función para procesar las líneas de datos
def procesar_lineas(lineas):
    datos = []
    for linea in lineas:
        partes = linea.split()[2:]  # Ignorar las dos primeras columnas
        datos.append([int(dato) if dato != "-999" else np.nan for dato in partes])
    return datos

# Función para calcular estadísticas
def calcular_estadisticas(datos):
    # Calcular el porcentaje de datos faltantes
    total_datos = datos.size
    datos_faltantes = np.isnan(datos).sum()
    porcentaje_faltantes = (datos_faltantes / total_datos) * 100

    # Reemplazar NaN por 0 para cálculos de estadísticas
    datos = np.nan_to_num(datos, nan=0)

    # Calcular estadísticas anuales
    precipitacion_anual = datos.sum(axis=1)
    media_anual = datos.mean(axis=1)

    # Calcular la tendencia de cambio anual
    tendencia_anual = np.diff(precipitacion_anual)

    # Encontrar los años más plujosos y más secs
    año_mas_plujoso = np.argmax(precipitacion_anual)
    año_mas_sec = np.argmin(precipitacion_anual)

    # Calcular estadísticas adicionales
    max_diario = datos.max(axis=1)
    min_diario = datos.min(axis=1)

    return {
        "porcentaje_faltantes": porcentaje_faltantes,
        "precipitacion_anual": precipitacion_anual,
        "media_anual": media_anual,
        "tendencia_anual": tendencia_anual,
        "año_mas_plujoso": año_mas_plujoso,
        "año_mas_sec": año_mas_sec,
        "max_diario": max_diario,
        "min_diario": min_diario
    }

# Recorrer todos los archivos en la carpeta
datos_totales = []
max_length = 0
for filename in os.listdir(folder_path):
    if filename.endswith(".dat"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            lineas = file.readlines()[2:]  # Ignorar las dos primeras líneas
            datos = procesar_lineas(lineas)
            max_length = max(max_length, max(len(d) for d in datos))
            datos_totales.append(datos)

# Pad arrays to ensure they have the same number of columns
for i in range(len(datos_totales)):
    for j in range(len(datos_totales[i])):
        if len(datos_totales[i][j]) < max_length:
            datos_totales[i][j] += [np.nan] * (max_length - len(datos_totales[i][j]))

# Convert to numpy array
datos_totales = np.array([item for sublist in datos_totales for item in sublist])

# Calcular estadísticas globales
estadisticas = calcular_estadisticas(datos_totales)

# Mostrar resultados
print(f"Porcentaje de datos faltantes: {estadisticas['porcentaje_faltantes']:.2f}%")
print(f"Precipitación total anual: {estadisticas['precipitacion_anual']}")
print(f"Media anual de precipitaciones: {estadisticas['media_anual']}")
print(f"Tendencia anual de cambio: {estadisticas['tendencia_anual']}")
print(f"Año más plujoso: {estadisticas['año_mas_plujoso']}")
print(f"Año más seco: {estadisticas['año_mas_sec']}")
print(f"Máximo diario por año: {estadisticas['max_diario']}")
print(f"Mínimo diario por año: {estadisticas['min_diario']}")