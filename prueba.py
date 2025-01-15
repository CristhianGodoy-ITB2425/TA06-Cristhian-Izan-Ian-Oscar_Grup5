import os
import re

# Ruta de la carpeta PRECIPITACIONS
carpeta = "/home/cristhian.godoy.7e6/PycharmProjects/TA06-Cristhian-Izan-Ian-Oscar_Grup5/PRECIPITACIONS"
extensio = ".dat"
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