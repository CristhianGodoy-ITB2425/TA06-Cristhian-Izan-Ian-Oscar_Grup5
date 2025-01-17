import os
import re

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
        return bool(patro_linia_dades.match(linia))

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

        if any_mes_anterior is not None:
            anterior_any, anterior_mes = any_mes_anterior
            if actual_any < anterior_any or (actual_any == anterior_any and actual_mes != anterior_mes + 1):
                return f"Error: Seqüència incorrecta a la línia {i} - {linia.strip()}"

        any_mes_anterior = (actual_any, actual_mes)

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

                # Validar format línia per línia
                for i, linia in enumerate(linies, start=1):
                    linia = linia.strip()
                    if not validar_format_linia(linia, i):
                        error_msg = f"Fitxer {arxiu}: Error al format de la línia {i} - {linia}"
                        log.write(error_msg + "\n")
                        errors.append(error_msg)
                        break

                # Validar la seqüència de les dades
                error_sequencia = validar_sequencia(linies)
                if error_sequencia:
                    log.write(f"Fitxer {arxiu}: {error_sequencia}\n")
                    errors.append(f"Fitxer {arxiu}: {error_sequencia}")

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