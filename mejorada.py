import os
import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Ruta de la carpeta PRECIPITACIONS
carpeta = "./PRECIPITACIONS"
extensio = ".dat"

# Fitxer de log d'errors
fitxer_errors = "Error_log.log"

# Llista per emmagatzemar els errors
errors = []

# Patrons per validar línies
patro_primera_linia = re.compile(r'^precip\s+\S+\s+\S+\s+\S+\s+\S+\s+\d+$')
patro_segona_linia = re.compile(r'^P\d+\s+[\d.-]+\s+[\d.-]+\s+\d+\s+\S+\s+\d+\s+\d+\s+[\d-]+$')
patro_linia_dades = re.compile(r'^P\d+\s+\d+\s+\d+\s+(-?\d+\s+)*-?\d+$')

# Funció per validar el format de les línies
def validar_format_linia(linia, numero_linia):
    if numero_linia == 1:
        return bool(patro_primera_linia.match(linia))
    elif numero_linia == 2:
        return bool(patro_segona_linia.match(linia))
    else:
        return bool(patro_linia_dades.match(linia)) and '  ' not in linia

# Funció per validar la seqüència de les dades
def validar_sequencia(linies):
    primer_apartat = None
    any_mes_anterior = None

    for i, linia in enumerate(linies[2:], start=3):
        parts = linia.strip().split()
        actual_primer_apartat = parts[0]
        actual_any = int(parts[1])
        actual_mes = int(parts[2])

        if primer_apartat is None:
            primer_apartat = actual_primer_apartat
        elif actual_primer_apartat != primer_apartat:
            return f"Error: El primer apartat canvia a la línia {i} - {linia.strip()}"

        if actual_mes < 1 or actual_mes > 12:
            return f"Error: Mes invàlid a la línia {i} - {linia.strip()}"

        if any_mes_anterior is not None:
            anterior_any, anterior_mes = any_mes_anterior
            if actual_any < anterior_any or (actual_any == anterior_any and actual_mes != anterior_mes + 1):
                return f"Error: Seqüència incorrecta a la línia {i} - {linia.strip()}"

        any_mes_anterior = (actual_any, actual_mes)

    return None

# Funció per registrar errors
def registrar_error(error_msg):
    with open(fitxer_errors, 'a') as log:
        log.write(error_msg + "\n")
    errors.append(error_msg)

# Obrim el fitxer de registre per guardar els errors
with open(fitxer_errors, 'w') as log:
    log.write("Registre d'errors en la validació dels fitxers:\n")
    log.write("=" * 50 + "\n")

# Processar tots els fitxers a la carpeta
for arxiu in os.listdir(carpeta):
    if arxiu.endswith(extensio):
        ruta_fitxer = os.path.join(carpeta, arxiu)
        try:
            with open(ruta_fitxer, 'r') as fitxer:
                linies = fitxer.readlines()

            # Validar format línia per línia
            for i, linia in enumerate(linies, start=1):
                linia = linia.strip()
                if not validar_format_linia(linia, i):
                    error_msg = f"{datetime.now()}: Fitxer {arxiu}: Error al format de la línia {i} - {linia}"
                    registrar_error(error_msg)
                    break

            # Validar la seqüència de les dades
            error_sequencia = validar_sequencia(linies)
            if error_sequencia:
                error_msg = f"{datetime.now()}: Fitxer {arxiu}: {error_sequencia}"
                registrar_error(error_msg)

        except Exception as e:
            error_msg = f"{datetime.now()}: Fitxer {arxiu}: Error al llegir el fitxer - {e}"
            registrar_error(error_msg)

# Informar a la consola si hi ha errors
if errors:
    print("Errors detectats. Consulta el fitxer Error_log.log per més detalls.")
else:
    print("Tots els fitxers tenen el format correcte.")

# Leer los archivos de la carpeta y cargarlos en un DataFrame de Pandas
data = []
for arxiu in os.listdir(carpeta):
    if arxiu.endswith(extensio):
        ruta_fitxer = os.path.join(carpeta, arxiu)
        try:
            with open(ruta_fitxer, 'r') as fitxer:
                linies = fitxer.readlines()
                for linia in linies[2:]:
                    parts = linia.strip().split()
                    estacio = parts[0]
                    any = int(parts[1])
                    dades = [int(d) if d != "-999" else None for d in parts[2:]]
                    data.append([estacio, any] + dades)
        except Exception as e:
            print(f"Error al llegir el fitxer {arxiu}: {e}")

# Funció per comptar les dades i els dies sense registre
def comptar_dades_i_dies_sense_registre(ruta_fitxer):
    num_dades = 0
    dies_sense_registre = 0
    precipitacions_per_any = {}
    precipitacions_per_mes = {}
    precipitacions_per_estacio = {}

    with open(ruta_fitxer, 'r') as fitxer:
        linies = fitxer.readlines()

        # Processar les línies a partir de la tercera
        for linia in linies[2:]:
            parts = linia.strip().split()
            estacio = parts[0]
            any = int(parts[1])
            mes = int(parts[2])
            dades = [int(x) for x in parts[3:] if x != '-999']
            num_dades += len(parts[3:])  # Contar todas las columnas de datos
            dies_sense_registre += parts[3:].count('-999')

            if any not in precipitacions_per_any:
                precipitacions_per_any[any] = []
            precipitacions_per_any[any].extend(dades)

            if any not in precipitacions_per_mes:
                precipitacions_per_mes[any] = {}
            if mes not in precipitacions_per_mes[any]:
                precipitacions_per_mes[any][mes] = 0
            precipitacions_per_mes[any][mes] += sum(dades)

            if any not in precipitacions_per_estacio:
                precipitacions_per_estacio[any] = {}
            if estacio not in precipitacions_per_estacio[any]:
                precipitacions_per_estacio[any][estacio] = 0
            precipitacions_per_estacio[any][estacio] += sum(dades)

    return num_dades, dies_sense_registre, precipitacions_per_any, precipitacions_per_mes, precipitacions_per_estacio

# Variables globals per acumular els resultats
total_dades = 0
total_dies_sense_registre = 0
precipitacions_totals_per_any = {}
precipitacions_totals_per_mes = {}
precipitacions_totals_per_estacio = {}

# Processar tots els fitxers a la carpeta
for arxiu in os.listdir(carpeta):
    if arxiu.endswith(extensio):
        ruta_fitxer = os.path.join(carpeta, arxiu)
        num_dades, dies_sense_registre, precipitacions_per_any, precipitacions_per_mes, precipitacions_per_estacio = comptar_dades_i_dies_sense_registre(ruta_fitxer)
        total_dades += num_dades
        total_dies_sense_registre += dies_sense_registre

        for any, precipitacions in precipitacions_per_any.items():
            if any not in precipitacions_totals_per_any:
                precipitacions_totals_per_any[any] = []
            precipitacions_totals_per_any[any].append(sum(precipitacions) / len(precipitacions))

        for any, mesos in precipitacions_per_mes.items():
            if any not in precipitacions_totals_per_mes:
                precipitacions_totals_per_mes[any] = {}
            for mes, precipitacio in mesos.items():
                if mes not in precipitacions_totals_per_mes[any]:
                    precipitacions_totals_per_mes[any][mes] = 0
                precipitacions_totals_per_mes[any][mes] += precipitacio

        for any, estacions in precipitacions_per_estacio.items():
            if any not in precipitacions_totals_per_estacio:
                precipitacions_totals_per_estacio[any] = {}
            for estacio, precipitacio in estacions.items():
                if estacio not in precipitacions_totals_per_estacio[any]:
                    precipitacions_totals_per_estacio[any][estacio] = 0
                precipitacions_totals_per_estacio[any][estacio] += precipitacio

# Calcular el percentatge de dies sense registre
percentatge_dies_sense_registre = (total_dies_sense_registre / total_dades) * 100 if total_dades > 0 else 0

# Calcular el promig anual de precipitacions per a tot el país
promig_anual_per_pais = {}
for any, promigs in precipitacions_totals_per_any.items():
    total_precipitacions = sum(promigs)
    promig_anual = total_precipitacions / 372  # Dividir por 365 días en lugar de la cantidad de datos
    promig_anual_per_pais[any] = promig_anual

# Calcular el percentatge de canvi any a any
percentatges_canvi = []
anys_ordenats = sorted(promig_anual_per_pais.keys())
for i in range(1, len(anys_ordenats)):
    any_anterior = anys_ordenats[i - 1]
    any_actual = anys_ordenats[i]
    promig_anterior = promig_anual_per_pais[any_anterior]
    promig_actual = promig_anual_per_pais[any_actual]
    percentatge_canvi = ((promig_actual - promig_anterior) / promig_anterior) * 100
    percentatges_canvi.append(percentatge_canvi)

# Calcular la desviació estàndard del percentatge de canvi
desviacio_estandar = sum(percentatges_canvi) / len(percentatges_canvi) if percentatges_canvi else 0

# Calcular el mes més plujós de cada any
mes_mes_plujos_per_any = {}
for any, mesos in precipitacions_totals_per_mes.items():
    mes_mes_plujos = max(mesos, key=mesos.get)
    mes_mes_plujos_per_any[any] = mes_mes_plujos

# Calcular la estació més plujosa de cada any
estacio_mes_plujosa_per_any = {}
for any, estacions in precipitacions_totals_per_estacio.items():
    estacio_mes_plujosa = max(estacions, key=estacions.get)
    estacio_mes_plujosa_per_any[any] = estacio_mes_plujosa

# Identificar los años más lluviosos y más secos
any_mes_plujos = max(promig_anual_per_pais, key=promig_anual_per_pais.get)
any_mes_sec = min(promig_anual_per_pais, key=promig_anual_per_pais.get)

# Funció per mostrar els resultats en una nova finestra amb un gràfic
def mostrar_resultats():
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # Gràfic de barres per les precipitacions anuals
    anys = list(promig_anual_per_pais.keys())
    precipitacions = list(promig_anual_per_pais.values())
    axs[0, 0].bar(anys, precipitacions)
    axs[0, 0].set_xlabel("Any")
    axs[0, 0].set_ylabel("Precipitacions (litres)")
    axs[0, 0].set_title("Promig anual de precipitacions per a tot el país")

    # Gràfic de línia per la desviació estàndard del percentatge de canvi
    axs[0, 1].plot(anys_ordenats[1:], percentatges_canvi, marker='o')
    axs[0, 1].set_xlabel("Any")
    axs[0, 1].set_ylabel("Percentatge de canvi (%)")
    axs[0, 1].set_title("Percentatge de canvi any a any")

    # Gràfic de barres per el mes més plujós de cada any
    mesos = list(mes_mes_plujos_per_any.values())
    axs[1, 0].bar(anys, mesos)
    axs[1, 0].set_xlabel("Any")
    axs[1, 0].set_ylabel("Mes")
    axs[1, 0].set_title("Mes més plujós de cada any")

    # Gràfic de barres per l'estació més plujosa de cada any
    estacions = list(estacio_mes_plujosa_per_any.values())
    axs[1, 1].bar(anys, estacions)
    axs[1, 1].set_xlabel("Any")
    axs[1, 1].set_ylabel("Estació")
    axs[1, 1].set_title("Estació més plujosa de cada any")

    plt.tight_layout()
    plt.show()

# Imprimir els resultats totals
print(f"Total nombre de dades: {total_dades}")
print(f"Total dies sense registre: {total_dies_sense_registre}")
print(f"Percentatge de dies sense registre: {percentatge_dies_sense_registre:.2f}%")
print("Promig anual de precipitacions per a tot el país:")
for any, promig in sorted(promig_anual_per_pais.items()):
    print(f"  {any}: {promig:.2f} litres")
print(f"Desviació estàndard del percentatge de canvi: {desviacio_estandar:.2f}%")
print("Mes més plujós de cada any:")
for any, mes in sorted(mes_mes_plujos_per_any.items()):
    print(f"  {any}: {mes}")
print("Estació més plujosa de cada any:")
for any, estacio in sorted(estacio_mes_plujosa_per_any.items()):
    print(f"  {any}: {estacio}")
print(f"Año más lluvioso: {any_mes_plujos} ({promig_anual_per_pais[any_mes_plujos]:.2f} litros)")
print(f"Año más seco: {any_mes_sec} ({promig_anual_per_pais[any_mes_sec]:.2f} litros)")

# Mostrar els resultats en una nova finestra amb un gràfic
mostrar_resultats()