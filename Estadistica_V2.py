import os

# Ruta de la carpeta PRECIPITACIONS
carpeta = "./PRECIPITACIONS"
extensio = ".dat"

# Funció per comptar les dades i els dies sense registre
def comptar_dades_i_dies_sense_registre(ruta_fitxer):
    num_dades = 0
    dies_sense_registre = 0
    precipitacions_per_any = {}

    with open(ruta_fitxer, 'r') as fitxer:
        linies = fitxer.readlines()

        # Processar les línies a partir de la tercera
        for linia in linies[2:]:
            parts = linia.strip().split()
            any = int(parts[1])
            dades = [int(x) for x in parts[3:] if x != '-999']
            num_dades += len(parts[3:])  # Contar todas las columnas de datos
            dies_sense_registre += parts[3:].count('-999')

            if any not in precipitacions_per_any:
                precipitacions_per_any[any] = []
            precipitacions_per_any[any].extend(dades)

    return num_dades, dies_sense_registre, precipitacions_per_any

# Variables globals per acumular els resultats
total_dades = 0
total_dies_sense_registre = 0
precipitacions_totals_per_any = {}

# Processar tots els fitxers a la carpeta
for arxiu in os.listdir(carpeta):
    if arxiu.endswith(extensio):
        ruta_fitxer = os.path.join(carpeta, arxiu)
        num_dades, dies_sense_registre, precipitacions_per_any = comptar_dades_i_dies_sense_registre(ruta_fitxer)
        total_dades += num_dades
        total_dies_sense_registre += dies_sense_registre

        for any, precipitacions in precipitacions_per_any.items():
            if any not in precipitacions_totals_per_any:
                precipitacions_totals_per_any[any] = []
            precipitacions_totals_per_any[any].append(sum(precipitacions) / len(precipitacions))

# Calcular el percentatge de dies sense registre
percentatge_dies_sense_registre = (total_dies_sense_registre / total_dades) * 100 if total_dades > 0 else 0

# Calcular el promig anual de precipitacions per a tot el país
promig_anual_per_pais = {any: sum(promigs) / len(promigs) for any, promigs in precipitacions_totals_per_any.items()}

# Imprimir els resultats totals
print(f"Total nombre de dades: {total_dades}")
print(f"Total dies sense registre: {total_dies_sense_registre}")
print(f"Percentatge de dies sense registre: {percentatge_dies_sense_registre:.2f}%")
print("Promig anual de precipitacions per a tot el país per dia:")
for any, promig in sorted(promig_anual_per_pais.items()):
    print(f"  {any}: {promig:.2f} l/dia")