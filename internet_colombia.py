
import pandas as pd
from pandasgui import show
import seaborn as sns
import matplotlib.pyplot as plt

# 1) Subir archivo

# Definir la ruta del archivo CSV
data = r"C:/Users/killa/Downloads/internet_penetracion.csv"

# 1.1) Leer el CSV desde el archivo
df = pd.read_csv(data)
print("\nPrimeros datos cargados:")
print(df.head())
print(" ")

# 2) Limpieza de datos:

# 2.1) Eliminamos columnas que no necesitamos
df.drop(columns=["COD_DEPARTAMENTO", "COD_MUNICIPIO"], inplace=True)
print("\nElimino columnas innecesarias:")
print(df.head())
print(" ")

# 2.2) Renombrar columnas
print("\nRenombro columnas:")
df.rename(columns={"No. ACCESOS FIJOS A INTERNET": "ACCESOS"}, inplace=True)
print(df.head())
print(" ")

# 2.3) Ordenar por año en forma ascendente
df.sort_values(by="AÑO", ascending=True, inplace=True)
print("\nOrdeno por año en forma ascendente:")
print(df.head())
print(" ")

# 2.4) Función para identificar valores incorrectos y formato
def identificar_valores_incorrectos_y_formato(df):
    resultados = {}
    # 2.4.1)
    # Identificar valores nulos
    resultados['valores_nulos'] = df.isnull().sum()

    # 2.4.2)
    # Identificar duplicados
    resultados['duplicados'] = df.duplicated().sum()
    
    #2.4.3)
    # Identificar columnas con tipos incorrectos
    resultados['tipos_incorrectos'] = {}
    for columna in df.columns:
        try:
            pd.to_numeric(df[columna])
        except ValueError:
            resultados['tipos_incorrectos'][columna] = True
    #2.4.4
    # Identificar formato de texto
    resultados['formato_texto'] = pd.DataFrame(columns=['Columna', 'Letra Capital', 'Todo Mayúscula', 'Todo Minúscula'])
    
    for columna in df.columns:
        if df[columna].dtype == 'object':  # Asegurarse de que la columna sea de tipo texto
            letra_capital = df[columna].str.match(r'^[A-Z][a-z]*$').sum()
            todo_mayuscula = df[columna].str.isupper().sum()
            todo_minuscula = df[columna].str.islower().sum()
            resultados['formato_texto'] = pd.concat([
                resultados['formato_texto'],
                pd.DataFrame({
                    'Columna': [columna],
                    'Letra Capital': [letra_capital],
                    'Todo Mayúscula': [todo_mayuscula],
                    'Todo Minúscula': [todo_minuscula]
                })
            ], ignore_index=True)
    
    return resultados

# 2.5)  Identificar valores incorrectos y formato en el DataFrame
resultados = identificar_valores_incorrectos_y_formato(df)
print("\nResultados de identificación de valores incorrectos y formato:")
print(resultados['formato_texto'])

print("\nValores nulos:")
print(resultados['valores_nulos'])

print("\nDuplicados:")
print(resultados['duplicados'])

# 3) Estadistica Descriptiva


# 3.1)Calcular estadísticas básicas y cuartiles
print("\nEstadísticas básicas:")
print(df.describe())

cuartiles = [0.25, 0.5, 0.75]  # Percentiles 25%, 50%, 75%
cuartiles_values = df['ACCESOS'].quantile(cuartiles)
cuartiles_df = pd.DataFrame({
    'Cuartil': [f'{int(p*100)}%' for p in cuartiles],
    'Value': cuartiles_values
})

print("\nCuartiles Calculados:")
print(cuartiles_df)
print(" ")


# 3.2) Top 10 de mayores acessos.
# 3.2.1) Agrupar por Departamento y Municipio, sumar accesos
accesos_por_municipio = df.groupby(["DEPARTAMENTO", "MUNICIPIO"])["ACCESOS"].sum().reset_index()

# 3.2.2) Ordenar de mayor a menor
top_10_municipios = accesos_por_municipio.sort_values(by="ACCESOS", ascending=False).head(10)

print("\nTop 10 ciudades y departamentos con mayor número de accesos a Internet:")
print(top_10_municipios)


# 3.3) Solo los 10 departamentos.

accesos_por_departamento = df.groupby("DEPARTAMENTO")["ACCESOS"].sum().reset_index()

# 3.3.1) Ordenar de mayor a menor
top_10_departamentos = accesos_por_departamento.sort_values(by="ACCESOS", ascending=False).head(10)

print("\nTop 10 departamentos con mayor número de accesos a Internet:")
print(top_10_departamentos)

# 3.4) Top 10 de las ciudades con Mayor acesso
accesos_por_ciudad = df.groupby("MUNICIPIO")["ACCESOS"].sum().reset_index()


# 3.4.1) Ordenar de mayor a menor
top_10_ciudades = accesos_por_ciudad.sort_values(by="ACCESOS", ascending=False).head(10)




print("\nTop 10 ciudades con menor número de accesos a Internet:")
print("bottom_10_ciudades")

# 3.5) departamentos con menores accesos.
# Agrupar por departamento y sumar accesos
accesos_por_departamento = df.groupby("DEPARTAMENTO")["ACCESOS"].sum().reset_index()

# Ordenar de menor a mayor
bottom_departamentos = accesos_por_departamento.sort_values(by="ACCESOS", ascending=True).head(10)

print("\nTop 10 departamentos con menor número de accesos a Internet:")
print(bottom_departamentos)

#Verificaremos si existen datos con valores nulos o igual a cero en el datatset y los filtraremos
accesos_por_departamento = accesos_por_departamento[accesos_por_departamento["ACCESOS"] > 0]


# 3.7) TOP 10 DE Ciudades y departamentos de menos conectividad
accesos_por_municipio = df.groupby(["DEPARTAMENTO", "MUNICIPIO"])["ACCESOS"].sum().reset_index()

# Filtrar accesos mayores a 0 para evitar errores de registro (opcional)
accesos_por_municipio = accesos_por_municipio[accesos_por_municipio["ACCESOS"] > 0]

# Ordenar de menor a mayor
bottom_10_municipios = accesos_por_municipio.sort_values(by="ACCESOS", ascending=True).head(10)

print("\nTop 10 ciudades con menor número de accesos a Internet (con sus departamentos):")
print(bottom_10_municipios)

#Indice de las ciudades con menor acceso 

# Ordenar el DataFrame por la columna "INDICE" de menor a mayor y seleccionar las 10 primeras filas
bottom_10_ciudades_indice = df.sort_values(by="INDICE", ascending=True).head(10)

# Mostrar solo las columnas relevantes: Departamento, Municipio e Índice
bottom_10_ciudades_indice_list = bottom_10_ciudades_indice[["DEPARTAMENTO", "MUNICIPIO", "INDICE"]]


print(bottom_10_ciudades_indice_list)

#Indice de las ciudades con Myor acceso

# Ordenar el DataFrame por la columna "INDICE" de mayor a menor y seleccionar las 10 primeras filas
top_10_ciudades_indice = df.sort_values(by="INDICE", ascending=False).head(10)

# Mostrar solo las columnas relevantes: Departamento, Municipio e Índice
top_10_ciudades_indice_list = top_10_ciudades_indice[["DEPARTAMENTO", "MUNICIPIO", "INDICE"]]

print(top_10_ciudades_indice_list)

#Ciudad con mayor Indice
max_indice_row = df.loc[df['INDICE'].idxmax()]
print("Ciudad con mayor índice de penetración de internet:")
print(f"{max_indice_row['MUNICIPIO']} - {max_indice_row['INDICE']}%")



indice_max = df['INDICE'].idxmax()

print(f"La ciudad con mayor índice de penetración está en la fila: {indice_max}")
print(df.loc[indice_max])

# 4) Graficar
# 4.1)
print("\nTop 10 ciudades con mayor número de accesos a Internet:")
print(top_10_ciudades)
plt.figure(figsize = (16,4))
plt.title("Municipios con mayor conectividad")
sns.barplot( x = top_10_ciudades["MUNICIPIO"], y = top_10_ciudades["ACCESOS"])
plt.xlabel("Ciudad", fontsize = 8)
plt.ylabel("Numero de conexiones", fontsize = 8)



# Agrupar por ciudad (municipio) y sumar accesos
accesos_por_ciudad = df.groupby("MUNICIPIO")["ACCESOS"].sum().reset_index()

# Ordenar de menor a mayor
bottom_10_ciudades = accesos_por_ciudad.sort_values(by="ACCESOS", ascending=True).head(10)

 
#  4.2) Municipios mayor conectividad 
plt.figure(figsize = (16,4))
plt.title("Municipios con menor conectividad")
sns.barplot( x = bottom_10_ciudades["MUNICIPIO"], y = bottom_10_ciudades["ACCESOS"])
plt.xlabel("Ciudad", fontsize = 8)
plt.ylabel("Numero de conexiones", fontsize = 8)

# 4.3) Dispersion
sns.relplot( x = "POBLACIÓN DANE" , y = "ACCESOS", data = df)
sns.set_style("darkgrid")
plt.title("Dispersion Población Vs Conectividad")
#plt.show() 
#gui = show(data)



# 4.4) 
#Visualizacion del crecimiento de accesos en el tiempo. (2015-2023)
print("Columnas disponibles:", df.columns)

# Filtrar por ciudad (municipio)
#municipio = "La Guadalupe"  # Cambia este valor por el municipio que desees analizar
municipio = input(str("Ingrese una ciudad en letras capitales: "))
df_ciudad = df[df['MUNICIPIO'].str.upper() == municipio.upper()]


# Crear una columna de fecha combinando AÑO y TRIMESTRE
df_ciudad['FECHA'] = df_ciudad['AÑO'].astype(str) + 'T' + df_ciudad['TRIMESTRE'].astype(str)

# Ordenar cronológicamente
df_ciudad = df_ciudad.sort_values(by=['AÑO', 'TRIMESTRE'])

# Graficar la evolución del índice de penetración
plt.figure(figsize=(12, 6))
plt.plot(df_ciudad['FECHA'], df_ciudad['INDICE'], marker='o', linestyle='-', color='blue')
plt.xticks(rotation=45)
plt.title(f'Evolución de la penetración de Internet fijo en {municipio}')
plt.xlabel('Fecha (Año - Trimestre)')
plt.ylabel('Índice de Penetración (%)')
plt.grid(True)
plt.tight_layout()
plt.show()