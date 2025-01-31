import os
import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import calendar

# ===================================================
# CONFIGURACIÓN
# ===================================================
CARPETA_DATOS = "./PRECIPITACIONS"
EXTENSION = ".dat"
LOG_ERRORES = "Error_log.log"
MESES = {i: calendar.month_abbr[i] for i in range(1, 13)}

# ===================================================
# PATRONES REGEX (VALIDACIÓN DE FORMATO)
# ===================================================
PATRON_CABECERA = re.compile(r'^precip\s+\S+\s+\S+\s+\S+\s+\S+\s+\d+$')
PATRON_METADATOS = re.compile(r'^P\d+\s+[\d.-]+\s+[\d.-]+\s+\d+\s+\S+\s+\d+\s+\d+\s+[\d-]+$')
PATRON_DATOS = re.compile(r'^P\d+\s+\d+\s+\d+\s+-?\d+(\s+-?\d+){30}$')


# ===================================================
# FUNCIONES DE VALIDACIÓN
# ===================================================
def validar_formato_linea(linea, num_linea):
    if num_linea == 1:
        return bool(PATRON_CABECERA.match(linea))
    elif num_linea == 2:
        return bool(PATRON_METADATOS.match(linea))
    else:
        if not bool(PATRON_DATOS.match(linea)):
            return False
        # Verificar que no tenga más de 31 días
        partes = linea.split()
        if len(partes[3:]) != 31:
            return False
        return True


def validar_secuencia(lineas):
    estacion_inicial = None
    anyo_actual = None
    mes_actual = None
    meses_presentados = set()

    for i, linea in enumerate(lineas[2:], start=3):
        partes = linea.strip().split()
        estacion = partes[0]
        anyo = int(partes[1])
        mes = int(partes[2])

        # Validar consistencia de la estación
        if estacion_inicial is None:
            estacion_inicial = estacion
        elif estacion != estacion_inicial:
            return f"Error: Cambio de estación en línea {i}"

        # Validar rango del mes
        if not (1 <= mes <= 12):
            return f"Error: Mes inválido ({mes}) en línea {i}"

        # Validar secuencia temporal
        if anyo_actual is not None:
            if anyo < anyo_actual:
                return f"Error: Año {anyo} menor que año anterior ({anyo_actual})"
            if anyo == anyo_actual and mes != mes_actual + 1:
                return f"Error: Mes {mes} no secuencial en línea {i}"

        anyo_actual = anyo
        mes_actual = mes
        meses_presentados.add(mes)

    if len(meses_presentados) != 12:
        meses_faltantes = set(range(1, 13)) - meses_presentados
        return f"Error: Meses incompletos. Faltan: {meses_faltantes}"

    return None


# ===================================================
# PROCESAMIENTO DE ARCHIVOS
# ===================================================
def procesar_archivos():
    errores = []
    datos = []
    total_dias = 0
    total_missing = 0

    with open(LOG_ERRORES, 'w') as log:
        log.write("Registro de errores:\n")
        log.write("=" * 50 + "\n")

        for archivo in os.listdir(CARPETA_DATOS):
            if not archivo.endswith(EXTENSION):
                continue

            ruta = os.path.join(CARPETA_DATOS, archivo)
            try:
                with open(ruta, 'r') as f:
                    lineas = f.readlines()

                # Validación de formato
                for num_linea, linea in enumerate(lineas, 1):
                    if not validar_formato_linea(linea.strip(), num_linea):
                        error = f"{datetime.now()}: Archivo {archivo} - Error formato línea {num_linea}"
                        errores.append(error)
                        log.write(error + "\n")
                        raise ValueError(error)

                # Validación de secuencia
                error_sec = validar_secuencia(lineas)
                if error_sec:
                    error = f"{datetime.now()}: Archivo {archivo} - {error_sec}"
                    errores.append(error)
                    log.write(error + "\n")
                    raise ValueError(error_sec)

                # Procesar datos válidos
                for linea in lineas[2:]:
                    partes = linea.strip().split()
                    estacion = partes[0]
                    anyo = int(partes[1])
                    mes = int(partes[2])

                    # Procesar los 31 días
                    for dia, valor in enumerate(partes[3:34], 1):  # Aseguramos 31 días
                        total_dias += 1
                        if valor == '-999':
                            total_missing += 1
                            continue

                        datos.append({
                            'Estación': estacion,
                            'Año': anyo,
                            'Mes': mes,
                            'Día': dia,
                            'Precipitación': float(valor)
                        })

            except Exception as e:
                error = f"{datetime.now()}: Error procesando {archivo} - {str(e)}"
                errores.append(error)
                log.write(error + "\n")

    df = pd.DataFrame(datos)
    return df, total_dias, total_missing, errores


# ===================================================
# ANÁLISIS DE DATOS
# ===================================================
def analizar_datos(df, total_dias, total_missing):
    resultados = {}

    # Estadísticas básicas
    resultados['Total días registrados'] = total_dias
    resultados['Total días sin dato'] = total_missing
    resultados['Porcentaje missing'] = (total_missing / total_dias * 100) if total_dias > 0 else 0

    # Precipitación anual promedio
    precipitation_annual = df.groupby('Año')['Precipitación'].agg(['sum', 'count'])
    resultados['Precipitación anual'] = precipitation_annual['sum'] / precipitation_annual['count'] * 365

    # Mes más lluvioso por año
    resultados['Mes más lluvioso'] = df.groupby(['Año', 'Mes'])['Precipitación'].sum().groupby('Año').idxmax().apply(
        lambda x: MESES[x[1]])

    # Estación más lluviosa por año
    resultados['Estación más lluviosa'] = df.groupby(['Año', 'Estación']).sum(numeric_only=True).groupby('Año').idxmax()

    # Variación interanual
    resultados['Variación anual'] = resultados['Precipitación anual'].pct_change() * 100

    return resultados


# ===================================================
# VISUALIZACIÓN
# ===================================================
def generar_graficos(resultados):
    plt.figure(figsize=(15, 10))

    # Gráfico de precipitación anual
    plt.subplot(2, 2, 1)
    resultados['Precipitación anual'].plot(kind='bar', color='skyblue')
    plt.title('Precipitación Media Anual (mm)')
    plt.xlabel('Año')
    plt.ylabel('Precipitación')

    # Gráfico de variación anual
    plt.subplot(2, 2, 2)
    resultados['Variación anual'].plot(kind='line', marker='o', color='green')
    plt.title('Variación Interanual (%)')
    plt.xlabel('Año')
    plt.ylabel('Porcentaje')
    plt.axhline(0, color='gray', linestyle='--')

    # Gráfico de meses más lluviosos
    plt.subplot(2, 2, 3)
    mes_colors = plt.cm.tab20(range(12))
    mes_patches = [mpatches.Patch(color=mes_colors[i], label=MESES[i + 1]) for i in range(12)]
    meses_data = resultados['Mes más lluvioso'].value_counts().reindex(MESES.values())
    meses_data.plot(kind='bar', color=mes_colors)
    plt.title('Distribución de Meses Más Lluviosos')
    plt.legend(handles=mes_patches, bbox_to_anchor=(1.05, 1))

    plt.tight_layout()
    plt.show()


# ===================================================
# EJECUCIÓN PRINCIPAL
# ===================================================
if __name__ == "__main__":
    df, total_dias, total_missing, errores = procesar_archivos()

    if not df.empty:
        resultados = analizar_datos(df, total_dias, total_missing)
        print("Resultados del análisis:")
        print(f"Datos totales procesados: {total_dias}")
        print(f"Días sin registro: {total_missing} ({resultados['Porcentaje missing']:.2f}%)")
        print("\nPrecipitación anual promedio:")
        print(resultados['Precipitación anual'].to_string())
        print("\nMeses más lluviosos por año:")
        print(resultados['Mes más lluvioso'].to_string())
        print("\nVariación interanual (%):")
        print(resultados['Variación anual'].to_string())

        generar_graficos(resultados)
    else:
        print("No se encontraron datos válidos para analizar.")

    if errores:
        print(f"\nSe encontraron {len(errores)} errores. Ver {LOG_ERRORES} para detalles.")
    else:
        print("\nTodos los archivos fueron procesados correctamente.")