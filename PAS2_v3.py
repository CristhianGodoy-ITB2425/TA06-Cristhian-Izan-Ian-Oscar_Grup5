import os
import re
from datetime import datetime

# Ruta de la carpeta PRECIPITACIONS
carpeta = "./Precipitacions_prova"
extensio = ".dat"

# Fitxer de log d'errors
fitxer_errors = "Error_log.log"

# Llista per emmagatzemar els errors
errors = []

# Patrons per validar línies
patro_linia_dades = re.compile(r'^P\d+\s+\d+\s+\d+\s+(-?\d+\s+){30}-?\d+$')

# Funció per validar el format de les línies
def validar_format_linia(linia):
    return bool(patro_linia_dades.match(linia))

# Funció per validar la seqüència de les dades
def validar_sequencia(linies):
    primer_apartat = None
    any_mes_anterior = None
    mesos_presentats = set()

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
            return f"Error: Mes fora de rang a la línia {i} - {linia.strip()}"

        mesos_presentats.add(actual_mes)

        if any_mes_anterior is not None:
            anterior_any, anterior_mes = any_mes_anterior
            if actual_any < anterior_any or (actual_any == anterior_any and actual_mes != anterior_mes + 1):
                return f"Error: Seqüència incorrecta a la línia {i} - {linia.strip()}"

        any_mes_anterior = (actual_any, actual_mes)

    if len(mesos_presentats) != 12:
        return f"Error: Falten mesos o hi ha mesos duplicats en el fitxer."

    return None

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

                # Validar format línia per línia a partir de la tercera línia
                for i, linia in enumerate(linies[2:], start=3):
                    linia = linia.strip()
                    if not validar_format_linia(linia):
                        error_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fitxer {arxiu}: Error al format de la línia {i} - {linia}"
                        log.write(error_msg + "\n")
                        errors.append(error_msg)

                # Validar la seqüència de les dades
                error_sequencia = validar_sequencia(linies)
                if error_sequencia:
                    log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fitxer {arxiu}: {error_sequencia}\n")
                    errors.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fitxer {arxiu}: {error_sequencia}")

                # Si totes les línies són correctes
                else:
                    print(f"Fitxer {arxiu}: Format correcte.")
            except Exception as e:
                error_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fitxer {arxiu}: Error al llegir el fitxer - {e}"
                log.write(error_msg + "\n")
                errors.append(error_msg)

# Informar a la consola si hi ha errors
if errors:
    print("Errors detectats. Consulta el fitxer Error_log.log per més detalls.")
else:
    print("Tots els fitxers tenen el format correcte.")