import pandas as pd
import matplotlib.pyplot as plt

#Ruta al archivo CSV
file_path = 'vgsales.csv'

#Cargar los datos
df = pd.read_csv(file_path)

############################
"Limpiamos los datos y los exportamos a un nuevo csv"

#Para cada fila con un N/A (inexistente), lo eliminamos y actualizamos la columna Rank para que quede adecuado, de otra forma dejaria inconsistentes los resultados y algunas funciones tiraria error
df = df.replace("N/A", pd.NA).dropna()
df["Rank"] = range(1, len(df) + 1)

#Exportamos el dataset limpio a un nuevo .csv para tenerlo listo
output_path = "dataset_limpio.csv"
df.to_csv(output_path, index=False)


############################
'''
El objetivo de este trabajo es el analisis del dataset: "Video Game Sales" (GregorySmith, 2018), donde planteamos distintas preguntas que pueden surgir
y el objetivo del mismo es llegar a los resultados. Los resultados se verán por el output con un formato de A hasta E, donde cada letra implica una 
pregunta distinta. Tambien se incluyeron distintos graficos para mejorar la visualizacion de los resultados y los analisis.


Preguntas a considerar:
    
A: ¿Cual consola vendio mas juegos en total?
B: ¿Que genero vendio mas juegos en total?
C: ¿Qué genero vendio mas en cada década? [0, x) 
D: ¿Qué genero se vende mas en cada región? 
E: ¿Qué empresa vendio mas en total?"
'''

############################

def Analisis(df):
    "A: Cuál consola vendio mas juegos en total? - Graficar por barras"
    
    #Agrupar por plataforma y sumar las ventas globales
    ventas_por_plataforma = df.groupby("Platform")["Global_Sales"].sum()
    
    #Encontrar la plataforma con mayores ventas globales
    top_plataforma = ventas_por_plataforma.idxmax()
    top_ventas_por_plataforma = ventas_por_plataforma.max()
     
    #Graficar los datos en forma de barras
    plt.figure(figsize=(12, 6))
    ventas_por_plataforma.sort_values(ascending=False).plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total de Ventas Globales por Consola', fontsize=16)
    plt.xlabel('Consola', fontsize=12)
    plt.ylabel('Ventas Globales (millones)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    
    ############################
    "B: ¿Qué genero vendio mas en total? - Grafico por barras" 
    
    
    #Agrupar por genero y sumar las ventas globales
    ventas_por_genero = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
    
    #Graficar los datos en forma de barras
    plt.figure(figsize=(12, 6))
    ventas_por_genero.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total de Ventas Globales por genero', fontsize=16)
    plt.xlabel('Genero', fontsize=12)
    plt.ylabel('Ventas Globales (millones)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    #Encontrar el genero más vendido
    top_genero = ventas_por_genero.idxmax()  #genero más vendido
    top_ventas_por_genero = ventas_por_genero.max()  #Ventas del genero más vendido
    
    ############################
    "C: ¿Qué genero vendio mas en cada década? [0, x) - Graficar por barras" 
    
    #Definir los rangos de años
    bins = [1980, 1990, 2000, 2010, 2017]
    labels = ['1980-1990', '1990-2000', '2000-2010', '2010-2017']
    
    #Crear una nueva columna con el rango de años al que pertenece cada registro
    df['Year_Range'] = pd.cut(df['Year'], bins=bins, labels=labels, right=False)
    
    #Calcular las ventas totales por rango de años y género
    ventas_por_genero_by_range = df.groupby(['Year_Range', 'Genre'], observed=True)['Global_Sales'].sum()
    top_genero_per_range = ventas_por_genero_by_range.groupby('Year_Range', observed=True).idxmax()    
    
    #Crear gráficos para cada década
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    for i, decade in enumerate(labels):
        ax = axes[i // 2, i % 2]
        sorted_sales = ventas_por_genero_by_range.loc[decade].sort_values(ascending=False)
        sorted_sales.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
        ax.set_title(f'Ventas Globales por genero ({decade})', fontsize=14)
        ax.set_xlabel('Genero', fontsize=12)
        ax.set_ylabel('Ventas Globales (millones)', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

    
    ############################
    "D: ¿Qué genero se vende mas en cada región? en total - Graficar por barras"
    
    
    #Agrupar por genero y sumar las ventas en cada región
    ventas_region_por_genero = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    
    #Encontrar el genero más vendido por región
    top_genero_by_region = ventas_region_por_genero.idxmax()
    

    #Graficar los resultados
    plt.figure(figsize=(10, 6))
    ventas_region_por_genero.max().plot(kind='bar', color=['skyblue', 'skyblue', 'skyblue', 'skyblue'])
    plt.title("Genero más vendido por región", fontsize=16)
    plt.xlabel("Región", fontsize=12)
    plt.ylabel("Ventas Globales (millones)", fontsize=12)
    plt.xticks(range(4), ['NA', 'EU', 'JP', 'Other'], rotation=0)
    
    #Añadir los nombres de los generos más vendidos encima de las barras para mejorar la comprension
    for i, v in enumerate(ventas_region_por_genero.max()):
        genre = top_genero_by_region.iloc[i]
        plt.text(i, v + 10, f'{genre} ({v:.2f}M)', ha='center', fontsize=10)
    plt.tight_layout()
    plt.show()
    
    
    ############################
    "E: ¿Qué empresa vendio mas en total? - Grafico por barras"
    
    #Calcular la empresa con mayores ventas totales
    ventas_por_empresas = df.groupby('Publisher')['Global_Sales'].sum()
    top_vendedor_empresa = ventas_por_empresas.idxmax()
    top_ventas_por_plataforma = ventas_por_empresas.max()
    
    #Graficar las ventas de las empresas y ordenarlas de mayor a menor
    plt.figure(figsize=(12, 6))
    ventas_por_empresas.sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Top 10 de Empresas con Más Ventas Globales', fontsize=16)
    plt.xlabel('Empresa', fontsize=12)
    plt.ylabel('Ventas Globales (millones)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    ############################
    #Presentacion de Resultados:
        
    #A:
    print("\n" + "="*100)
    print("A:" + "¿Cuál consola vendió más juegos en total?".center(100))
    print("="*100 + "\n")
    print(f"La consola que vendió más juegos en total es '{top_plataforma}' con {top_ventas_por_plataforma:.2f} millones de copias.")
    print("\n")
    
    #B:
    print("\n" + "="*100)
    print("B:" + "¿Qué género vendió más juegos en total?".center(100))
    print("="*100 + "\n")
    print(f"El género que vendió más juegos en total es '{top_genero}' con {top_ventas_por_genero:.2f} millones de copias.")
    print("\n")
    
    #C:
    print("\n" + "="*100)
    print("C:" + "¿Qué género vendió más en cada década?".center(100))
    print("="*100 + "\n")
    for decade in labels:
        top_genero_for_decade = top_genero_per_range[decade]
        top_ventas_por_plataforma_for_decade = ventas_por_genero_by_range.loc[top_genero_for_decade]
        print(f"En la década {decade}, el género más vendido es '{top_genero_for_decade[1]}' con {top_ventas_por_plataforma_for_decade:.2f} millones de copias.")
    print("\n")

    #D:
    print("\n" + "="*100 )
    print("D:" + "¿Qué género se vende más en cada región?".center(100))
    print("="*100 + "\n")
    for region in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']:
        top_genero = top_genero_by_region[region]
        top_ventas_por_plataforma = ventas_region_por_genero.loc[top_genero, region]
        print(f"En la región {region.replace('_', ' ')} el género más vendido es '{top_genero}' con {top_ventas_por_plataforma:.2f} millones de copias.")
    print("\n")
    
    #E:
    print("\n" + "="*100)
    print("E:" + "¿Qué empresa vendió más juegos en total?".center(100))
    print("="*100 + "\n")
    print(f"La empresa que vendió más juegos en total es '{top_vendedor_empresa}' con {top_ventas_por_plataforma:.2f} millones de copias.")
    print("="*100)
    print("\n")

Analisis(df)

