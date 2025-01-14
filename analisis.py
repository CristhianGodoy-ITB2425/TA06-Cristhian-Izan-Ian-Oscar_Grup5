import pandas as pd
import glob

# Function to review the format of the files
def revisar_format_detallat(fitxers):
    formats = []
    for fitxer in fitxers:
        try:
            with open(fitxer, 'r') as f:
                primera_linia = f.readline()
                if ',' in primera_linia:
                    delimitador = ','
                elif '\t' in primera_linia:
                    delimitador = '\t'
                elif ' ' in primera_linia:
                    delimitador = ' '
                else:
                    delimitador = None

                columnes = primera_linia.strip().split(delimitador)
                # Read additional lines to check for comments and consistency
                comentaris = []
                for _ in range(5):
                    linia = f.readline()
                    if linia.startswith('#'):
                        comentaris.append(linia.strip())
                    else:
                        break

                # Read the entire file to get data types
                df = pd.read_csv(fitxer, delimiter=delimitador, comment='#')
                tipus_dades = df.dtypes.to_dict()

                formats.append((fitxer, delimitador, len(columnes), columnes, comentaris, tipus_dades))
        except Exception as e:
            print(f"Error llegint el fitxer {fitxer}: {e}")
    return formats

# Function to validate formats
def validar_format(formats):
    primer_format = formats[0]
    errors = []
    for fitxer, delimitador, n_columnes, columnes, comentaris, tipus_dades in formats:
        if delimitador != primer_format[1] or n_columnes != primer_format[2]:
            errors.append(f"Format diferent a {fitxer}")
    return errors

# Function to clean and combine data
def netejar_fitxers(fitxers, delimitador, columnes_esperades):
    dades_combinades = []
    for fitxer in fitxers:
        try:
            df = pd.read_csv(fitxer, delimiter=delimitador, comment='#')
            if list(df.columns) != columnes_esperades:
                print(f"Columnes diferents a {fitxer}: {df.columns}")
                continue
            # Replace missing values (-999) with NaN
            df.replace(-999, pd.NA, inplace=True)
            dades_combinades.append(df)
        except Exception as e:
            print(f"Error llegint el fitxer {fitxer}: {e}")
    return pd.concat(dades_combinades, ignore_index=True)

# Main execution
if __name__ == "__main__":
    # List of files in the PRECIPITACIONS folder
    fitxers = glob.glob("PRECIPITACIONS/*.dat")

    # Step 1: Review detailed formats
    formats = revisar_format_detallat(fitxers)
    for fitxer, delimitador, n_columnes, columnes, comentaris, tipus_dades in formats:
        print(f"{fitxer}: Delimitador={delimitador}, NColumnes={n_columnes}, Columnes={columnes}, Comentaris={comentaris}, Tipus de dades={tipus_dades}")

    # Step 2: Validate formats
    errors = validar_format(formats)
    if errors:
        print("Errors de format:")
        print("\n".join(errors))
    else:
        print("Tots els fitxers tenen el mateix format.")

    # Step 3: Clean and combine data
    delimitador = formats[0][1]  # Assume all have the same format
    columnes_esperades = formats[0][3]
    dades = netejar_fitxers(fitxers, delimitador, columnes_esperades)

    # Show combined data
    print(dades)

# Additional implementation to verify that all files have the same format
def revisar_format(fitxers):
    formats = []
    for fitxer in fitxers:
        try:
            with open(fitxer, 'r') as f:
                primera_linia = f.readline()
                if ',' in primera_linia:
                    delimitador = ','
                elif '\t' in primera_linia:
                    delimitador = '\t'
                elif ' ' in primera_linia:
                    delimitador = ' '
                else:
                    delimitador = None

                columnes = primera_linia.strip().split(delimitador)
                formats.append((fitxer, delimitador, len(columnes), columnes))
        except Exception as e:
            print(f"Error llegint el fitxer {fitxer}: {e}")
    return formats

# Function to validate formats
def validar_format_basica(formats):
    primer_format = formats[0]
    errors = []
    for fitxer, delimitador, n_columnes, columnes in formats:
        if delimitador != primer_format[1] or n_columnes != primer_format[2]:
            errors.append(f"Format diferent a {fitxer}")
    return errors

# Main execution for basic validation
if __name__ == "__main__":
    # List of files in the PRECIPITACIONS folder
    fitxers = glob.glob("PRECIPITACIONS/*.dat")

    # Step 1: Review formats
    formats = revisar_format(fitxers)
    for fitxer, delimitador, n_columnes, columnes in formats:
        print(f"{fitxer}: Delimitador={delimitador}, NColumnes={n_columnes}, Columnes={columnes}")

    # Step 2: Validate formats
    errors = validar_format_basica(formats)
    if errors:
        print("Errors de format:")
        print("\n".join(errors))
    else:
        print("Tots els fitxers tenen el mateix format.")