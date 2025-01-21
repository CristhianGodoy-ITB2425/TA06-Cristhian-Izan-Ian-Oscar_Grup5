import os

# Ruta de la carpeta PRECIPITACIONS
carpeta = "./PRECIPITACIONS"
extensio = ".dat"

# Funció per comptar les dades i els dies sense registre
def comptar_dades_i_dies_sense_registre(ruta_fitxer):
    num_dades = 0
    dies_sense_registre = 0
    precipitacions_per_any = {}
    precipitacions_per_mes = {}

    with open(ruta_fitxer, 'r') as fitxer:
        linies = fitxer.readlines()

        # Processar les línies a partir de la tercera
        for linia in linies[2:]:
            parts = linia.strip().split()
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

    return num_dades, dies_sense_registre, precipitacions_per_any, precipitacions_per_mes

# Variables globals per acumular els resultats
total_dades = 0
total_dies_sense_registre = 0
precipitacions_totals_per_any = {}
precipitacions_totals_per_mes = {}

# Processar tots els fitxers a la carpeta
for arxiu in os.listdir(carpeta):
    if arxiu.endswith(extensio):
        ruta_fitxer = os.path.join(carpeta, arxiu)
        num_dades, dies_sense_registre, precipitacions_per_any, precipitacions_per_mes = comptar_dades_i_dies_sense_registre(ruta_fitxer)
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

# Calcular el percentatge de dies sense registre
percentatge_dies_sense_registre = (total_dies_sense_registre / total_dades) * 100 if total_dades > 0 else 0

# Calcular el promig anual de precipitacions per a tot el país
promig_anual_per_pais = {any: sum(promigs) / len(promigs) for any, promigs in precipitacions_totals_per_any.items()}

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

# Identificar los años más lluviosos y más secos
any_mes_plujos = max(promig_anual_per_pais, key=promig_anual_per_pais.get)
any_mes_sec = min(promig_anual_per_pais, key=promig_anual_per_pais.get)

# Imprimir els resultats totals
print(f"Total nombre de dades: {total_dades}")
print(f"Total dies sense registre: {total_dies_sense_registre}")
print(f"Percentatge de dies sense registre: {percentatge_dies_sense_registre:.2f}%")
print("Promig anual de precipitacions per a tot el país:")
for any, promig in sorted(promig_anual_per_pais.items()):
    print(f"  {any}: {promig:.2f} l/dia")
print(f"Desviació estàndard del percentatge de canvi: {desviacio_estandar:.2f}%")
print("Mes més plujós de cada any:")
for any, mes in sorted(mes_mes_plujos_per_any.items()):
    print(f"  {any}: {mes}")
print(f"Año más lluvioso: {any_mes_plujos} ({promig_anual_per_pais[any_mes_plujos]:.2f} l/dia)")
print(f"Año más seco: {any_mes_sec} ({promig_anual_per_pais[any_mes_sec]:.2f} l/dia)")