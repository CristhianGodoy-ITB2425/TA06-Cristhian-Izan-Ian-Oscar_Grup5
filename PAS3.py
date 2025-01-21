# hazme un codigo que contenga esto
# PAS 3 Netejar les dades:
# Assegurar que les dades no continguin errors, valors que falten o inconsistències:
# Lectura: Es pot utilitzar  pandas per gestionar els fitxers i gestionar errors de lectura.
# Verifica la consistència de les columnes: Assegurar que les dades a cada columna tenen el tipus esperat (numèric, data, etc.).
# Gestionar valors que falten o corruptes: Identifica i tracta dades nul·les o valors atípics.

import os
import re
import pandas as pd


# Ruta de la carpeta PRECIPITACIONS
carpeta = "./Precipitacions_prova"
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
        return bool(patro_linia_dades.match(linia))

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
                        error_msg = f"Fitxer {arxiu}: Error al format de la línia {i} - {linia}"
                        log.write(error_msg + "\n")
                        errors.append(error_msg)
                        break

                # Si totes les línies són correctes
                else:
                    print(f"Fitxer {arxiu}: Format correcte.")
            except Exception as e:
                error_msg = f"Fitxer {arxiu}: Error al llegir el fitxer - {e}"
                log.write(error_msg + "\n")
                errors.append(error_msg)

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


