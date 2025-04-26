import pandas as pd
import matplotlib as plt


df= pd.read_csv("C:/Users/killa/Downloads/internet_penetracion.csv")


#Limpiar nombres de columnas: quitar espacios, tildes, y caracteres especiales
df.rename(columns=lambda x: x.strip(), inplace=True) #Limpieza de datos( quitando espacios y tildes)
df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

df_grouped = df.groupby('MUNICIPIO')['No. ACCESOS FIJOS A INTERNET'].sum().sort_values(ascending=False)

print("Ciudades con mayor acceso a internet:") #Mayor acceso a internet
print(df_grouped.head(10))

print("Ciudades con menor acceso a internet:")
print(df_grouped.tail(10))

if 'MUNICIPIO' in df.columns and 'No. ACCESOS FIJOS A INTERNET' in df.columns:
    agrupado = df.groupby(['ANO', 'MUNICIPIO'])['No. ACCESOS FIJOS A INTERNET'].sum().reset_index()
    print(agrupado.head(35500))
else:
    raise ValueError("Columnas 'MUNICIPIO' o 'No. ACCESOS FIJOS A INTERNET' no están presentes.")

df.drop_duplicates(inplace=True)

# 4. Eliminar filas completamente vacías
df.dropna(how='all', inplace=True)

# 5. Llenar o manejar valores nulos en columnas clave
# Por ejemplo, si hay nulos en 'NO. ACCESOS FIJOS A INTERNET':
if 'NO. ACCESOS FIJOS A INTERNET' in df.columns:
    df['NO. ACCESOS FIJOS A INTERNET'] = pd.to_numeric(df['NO. ACCESOS FIJOS A INTERNET'], errors='coerce')
    df['NO. ACCESOS FIJOS A INTERNET'].fillna(0, inplace=True)

# 6. Limpiar espacios en texto (como MUNICIPIO)
if 'MUNICIPIO' in df.columns:
    df['MUNICIPIO'] = df['MUNICIPIO'].str.strip().str.title()

# 7. Revisar tipos de datos
print(df.dtypes)

# 8. Vista previa de los datos limpios
print(df.head())

df['ANO'] = pd.to_numeric(df['ANO'], errors='coerce').astype('Int64')

df.rename(columns={
    'NO. ACCESOS FIJOS A INTERNET': 'ACCESOS',
    'MUNICIPIO': 'CIUDAD',
    'ANO': 'AÑO',
    'INDICE': '% ACCESO',
    "POBLACION DANE": "HABITANTES"
}, inplace=True)
print(df.rename)


df.drop(columns=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'], inplace=True)

# Vista previa
print(df.head(10))

df_grouped = df.groupby('CIUDAD')['No. ACCESOS FIJOS A INTERNET'].sum().sort_values(ascending=False)

# Mostrar las primeras 10 ciudades con mayor acceso a internet
print("Ciudades con mayor acceso a internet:")
print(df_grouped.head(10))

print("Ciudades con menor acceso a internet:")
print(df_grouped.tail(10))

df_grouped = df.groupby('DEPARTAMENTO')['No. ACCESOS FIJOS A INTERNET'].sum().sort_values(ascending=False)

print("Departamentos con mayor acceso a internet:")
print(df_grouped.head(10))


"""df['% ACCESO'] = pd.to_numeric(df['% ACCESO'], errors='coerce')"""

# Encontrar la fila con el mayor índice
max_indice_row = df.loc[df['% ACCESO'].idxmax()]

# Mostrar la ciudad y su índice
print("Ciudad con mayor índice de penetración de internet:")
print(f"{max_indice_row['CIUDAD']} - {max_indice_row['% ACCESO']}%")


indice_max = df['% ACCESO'].idxmax()

print(f"La ciudad con mayor índice de penetración está en la fila: {indice_max}")
print(df.loc[indice_max])



