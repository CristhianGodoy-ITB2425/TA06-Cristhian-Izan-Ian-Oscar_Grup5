import os

# Ruta de la carpeta PRECIPITACIONS
carpeta = "./PRECIPITACIONS"
extensio = ".dat"

# Funció per comptar les dades i els dies sense registre
def comptar_dades_i_dies_sense_registre(ruta_fitxer):
    num_dades = 0
    dies_sense_registre = 0

    with open(ruta_fitxer, 'r') as fitxer:
        linies = fitxer.readlines()

        # Processar les línies a partir de la tercera
        for linia in linies[2:]:
            parts = linia.strip().split()[3:]  # Ignorar les tres primeres columnes (estació, any, mes)
            num_dades += len(parts)
            dies_sense_registre += parts.count('-999')

    return num_dades, dies_sense_registre

# Variables globals per acumular els resultats
total_dades = 0
total_dies_sense_registre = 0

# Processar tots els fitxers a la carpeta
for arxiu in os.listdir(carpeta):
    if arxiu.endswith(extensio):
        ruta_fitxer = os.path.join(carpeta, arxiu)
        num_dades, dies_sense_registre = comptar_dades_i_dies_sense_registre(ruta_fitxer)
        total_dades += num_dades
        total_dies_sense_registre += dies_sense_registre

# Calcular el percentatge de dies sense registre
percentatge_dies_sense_registre = (total_dies_sense_registre / total_dades) * 100 if total_dades > 0 else 0

# Imprimir els resultats totals
print(f"Total nombre de dades: {total_dades}")
print(f"Total dies sense registre: {total_dies_sense_registre}")
print(f"Percentatge de dies sense registre: {percentatge_dies_sense_registre:.2f}%")