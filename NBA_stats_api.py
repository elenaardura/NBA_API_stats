# Importo las librerías necesarias para realizar el programa
import requests
from fpdf import FPDF
import sys
import signal
import warnings
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Defino las url con las imagenes de los jugadores del equipo
fotos_equipo = ["https://cdn.nba.com/headshots/nba/latest/1040x760/1626220.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/203933.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1628410.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1630561.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/201142.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/201988.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1627732.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/202681.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/203925.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/202693.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1630556.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1629139.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1630549.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1630560.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/203552.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1631214.png?imwidth=1040&imheight=760", 
                "https://cdn.nba.com/headshots/nba/latest/1040x760/1629651.png?imwidth=1040&imheight=760"]

# Defino el diccionario con las abreviaturas de las columnas de las distintas tablas
abreviaturas = {'Name': 'Name', 'Games': 'G', 'Time': 'T', 'PersonalFouls': 'PF', 'Rebounds': 'R', 'Assists': 'A', 'Steals': 'S', 'BlockedShots': 'Blk', 'Points': 'Pts', 'PlusMinus': '+/-',
                    'FieldGoalsMade': 'FGM', 'FieldGoalsAttempted': 'FGA', 'FieldGoalsPercentage': 'FG%','ThreePointersMade': 'TPM', 'ThreePointersAttempted': 'TPA', 
                    'ThreePointersPercentage': 'TP%', 'FreeThrowsMade': 'FTM', 'FreeThrowsAttempted': 'FTA', 'FreeThrowsPercentage': 'FT%', 'OffensiveRebounds': 'OR', 'DefensiveRebounds': 'DR', 'OffensiveReboundsPercentage': 'OR%',
                    'DefensiveReboundsPercentage': 'DR%', 'TotalReboundsPercentage': 'R%'}

# Defino la clase del pdf que vamos a crear
class PDF(FPDF):
    def header(self): # Defino la cabecera del pdf
        # Si el logo de los nets no se encuentra en el directorio con el nombre indicado, guardo la imagen y la inserto en el pdf
        if not os.path.exists('logo BKN.png'):
            guardar_foto('logo BKN.png', "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/092012/brooklyn_nets_logo.png?itok=QSKWsapv")
        self.image('logo BKN.png', 180, 7, 20) 
        
    def footer(self): # Defino el pie de página del pdf
        self.set_y(-20)
        self.set_font('Times', 'I', 11) # Escribo en cursiva
        self.set_text_color(50) # Cambio el color a un gris más oscuro
        self.cell(0, 10, 'Elena Ardura Carnicero - Adquisición de Datos', 0, 0, 'C') 
        self.ln(6)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C') # Escribo el número de página
    
    def portada(self): # Defino la portada del pdf
        self.set_fill_color(255, 255, 255) # Defino el color blanco como el relleno para el rectangulo que voy a crear
        self.rect(32, 47, 146, 206, 'DF') # Defino el rectángulo grande
        self.rect(35, 50, 140, 200, 'DF') # Defino el rectángulo pequeño
        self.set_font('Times', 'B', 40) # Establezco la fuente y el tamaño de la letra del tipo 
        self.set_y(60) # Defino en que coordenada y comienzo a escribir
        self.cell(0, 40, 'BROOKLYN NETS', 0, 0, 'C') # Escribo el título de manera centrada y sin recuadrar
        self.ln(20) # Dejo un doble interliniado para escribir el subtítulo
        self.set_font_size(28) # Establezco la fuente y el tamaño de la letra del tipo 
        self.set_text_color(100) # Cambio el color del subtítulo a un gris
        self.cell(0, 30, 'TEMPORADA 2022', 0, 0, 'C') # Escribo el subtítulo de manera centrada y sin recuadrar
        self.image('logo BKN.png', 55, 120, 100) # Pinto el logo del equipo

    def imprimo_apartado(self, num, titulo, texto): # Defino el apartado que escribe un nuevo apartado en el pdf
        self.add_page() # Escribo cada apartado en una nueva página
        self.set_font('Times', 'U', 14) 
        self.set_text_color(0,0,0) 
        self.cell(0, 6, f'{num}. {titulo}', 0, 0, 'L') # Escribo el título del apartado
        self.ln(10)
        self.set_font('Times','', 11)
        self.multi_cell(150, 6, texto) # Escribo el párrafo que describe el apartado
        
    def tabla_basica(self,df, dict): # Defino la función que crea una tabla
        ancho_pagina = self.w-60 # Establezco el ancho de la tabla
        columnas, filas = list(df.columns), list(df.index) # Defino las columnas y las filas de la tabla
        # Defino el ancho de cada columna dividiendo el ancho disponible entre el número de columnas a escribir sin contar con la columna del nombre
        ancho_columna = (ancho_pagina - 30 ) / (len(columnas)-1) 
        self.set_font('times', 'B', 12)
        self.ln(7) 
        if dict == None: # Si la función no tiene un diccionario con las abreviaturas para las distintas columnas
            for col in columnas: # Escribo los nombres de las columnas en la primera fila de la tabla, distinguiendo el cuadro de texto del nombre que el del resto ya que será más grande
                if col == 'Name':
                    self.cell(30, 8, str(col), 1, 0, 'C')
                else: 
                    self.cell(ancho_columna, 8, str(col), 1, 0, 'C') 
        else: # Si por el contrario la función tiene un diccionario con las abreviaturas de las distintas columnas
            for col in columnas: # Escribo las abreviaturas de las columnas en la primera fila de la tabla
                if col == 'Name':
                    self.cell(30, 8, str(dict[col]), 1, 0, 'C')
                else:
                    self.cell(ancho_columna, 8, str(dict[col]), 1, 0, 'C') # Escribo el nombre de las columnas en negrita
        self.ln()
        self.set_font('times', '', 11)
        for fila in filas: # Escribo cada celda de la tabla con el contenido del dataframe que tiene la propia función
            for col in columnas:
                if col == 'Name':
                    self.cell(30, 8 , str(df.loc[fila, col]), 1, 0, 'C')
                else:
                    self.cell(ancho_columna, 8, str(df.loc[fila, col]), 1, 0, 'C') # Escribo cada entrada de la tabla
            self.ln()  
        

def handler_signal(signal, frame): # Creo una función que controle la salida del ctrl + c 
    print('[!] Cerrando el programa...')
    sys.exit()

signal.signal(signal.SIGINT, handler_signal)
warnings.filterwarnings('ignore') # Elimino los avisos de la terminal
pd.options.display.max_columns = None # Elimino el limite de columnas a mostrar por pantalla de los dataframes 

def guardar_foto(nombre, foto): # Defino la función que guarda las imagenes en el directorio
    imagen = requests.get(foto).content # Obtengo la imagen de la url indicada
    with open(nombre, 'wb') as handler: # Guardo la imagen con el nombre pasado como argumento a la función
	    handler.write(imagen)
         
def plantilla_jugadores(pdf, caracteristicas_jugador): # Defino la función que imprime la plantilla del equipo
    ancho_columna = (pdf.w - 60) / 3
    contador = 0
    pdf.set_font('Times', 'B', 11)
    while contador < len(caracteristicas_jugador):
        pdf.ln()
        for i in range(3): # Escribo en una misma fila tres nombres junto a su numero de equipacion
            if contador + i < len(caracteristicas_jugador):
                pdf.cell(ancho_columna, 10, f"{caracteristicas_jugador.loc[contador+i, 'Name']} ({caracteristicas_jugador.loc[contador+i, 'Jersey']})" , 0, 0 ,'C')
        pdf.ln()
        y = pdf.y
        for j in range(3): # Imprimo justo debajo de los nombres sus respectivas imagenes
            if contador + j < len(caracteristicas_jugador):
                pdf.image(f'jugador_{contador+j}.png', x = 35 + (ancho_columna)*j, y = y, w= ancho_columna-10, link = "https://www.nba.com/nets/roster")
        pdf.ln(20)
        contador += 3
    pdf.ln(20)
           
def crear_grafico_barras_apiladas(datos, xlabel, ylabel, titulo, nombre): # Defino la función que crea los gráficos de barras apiladas
    nombres_jugadores = datos['Name'] # Defino los nombres que aparecerán en el eje x
    datos_matriz = datos.iloc[:,1:].to_numpy().transpose() # Defino los datos para las barras
    colores = ['#52545A', '#969AA6'] # Defino los colores de las barras
    plt.figure(1, figsize=(13, 9)) # Defino la figura
    plt.rc('axes', axisbelow=True) # Fijo que el grid del gráfico esté por detrás de las barras
    for i in range(datos_matriz.shape[0]):
        # Por cada columna imprimo una barra superpuesta sobre la anterior acerca de los tiros encestados y los fallados, y así poder ver el total de tiros y la relacion de encestados y fallados
        plt.bar(nombres_jugadores, datos_matriz[i], bottom = np.sum(datos_matriz[:i], axis = 0), color = colores[i], label = list(datos.columns)[i+1])
    # Establezco las características del gráfico
    plt.title(titulo) # Defino el titulo del gráfico
    plt.xticks(rotation = 30, fontsize= 9) # Giro el nombre de los datos del eje x y establezco el tamaño de letra
    plt.xlabel(xlabel) # Defino el nombre del eje x
    plt.ylabel(ylabel) # Defino el nombre del eje y
    plt.legend() # Creo una legenda para saber que tamaño representa cada color
    plt.grid(linestyle = '--', linewidth = 1) # Fijo el estilo y el grosos de las lineas de fondo del gráfico 
    plt.savefig(nombre) # Guardo la figura
    plt.clf() # Borro los datos previos de la libreria matplotlib

def extract(url_stats, url_players, headers): # Defino la funcion que extrae los datos de la api 
    # Extraigo los datos de dos apis distintas
    response = requests.get(url_stats, headers = headers) 
    response2 = requests.get(url_players, headers = headers)
    return response, response2
    
def transform(response, response2): # Defino la funcion que transforma los datos
    info_extraida_stats = response.json() # Creo dos diccionario con los datos de cada api respectivamente
    info_extraida_players = response2.json()
    info_stats = pd.DataFrame(info_extraida_stats) # Con los diccionarios creo los dataframes con los que vamos a trabajar
    info_players = pd.DataFrame(info_extraida_players)
    info_players = info_players.sort_values(by = 'Jersey').reset_index().copy() # Ordeno la info de los jugadores por orden de numero en la equipacion (de menor a mayor)
    # Defino una lista con los nombres de los jugadores tanto nombre como apellido y que así coincida con el otro dataframe
    nombres = [info_players.loc[fila, 'FirstName'] +' ' +info_players.loc[fila, 'LastName'] for fila in range(len(info_players))]
    # En la columna de la fecha de nacimiento transformo el string al formato objeto tipo fecha y hora
    info_players['BirthDate'] = pd.to_datetime(info_players['BirthDate'])
    # Creo un dataframe con las caracteristicas relevantes de los jugadores
    caracteristicas_jugador = info_players[['Jersey', 'Weight', 'Height', 'Position', 'BirthCountry']].copy()
    caracteristicas_jugador.insert(0, 'Name', nombres) # Añado al nuevo df una primera columna con el nombre completo de los jugadores
    # La columna de la fecha de nacimiento la transformo para quedarme solo con la fecha sin la hora
    caracteristicas_jugador['BirthDate'] =info_players['BirthDate'].dt.strftime('%m/%d/%Y')
    # Para que el nombre de la columna del lugar de nacimiento no sea muy largo, lo transfromo
    caracteristicas_jugador = caracteristicas_jugador.rename(columns = {'BirthCountry': 'Country'}) 
    # Creo una lista con el tiempo que ha jugado cada jugador a lo largo de la temporada juntando las columnas de minutos y la de segundos
    tiempo = [str(info_stats.loc[fila, 'Minutes']) +'.'+ str(info_stats.loc[fila, 'Seconds']) for fila in range(len(info_stats))]
    info_stats['Time'] = tiempo # En el df con las estadisticas de los jugaodres en 2022, creo una columna con el tiempo total jugado
    info_stats = info_stats.sort_values(by= 'Points', ascending = False).reset_index().copy() # Ordeno el df por el numero de puntos obtenidos por cada jugador 
    return caracteristicas_jugador, info_stats

def load(info_stats, caracteristicas_jugador): # Defino la funcion que carga los datos en un pdf
    pdf = PDF('P', 'mm', 'A4') # Creo el pdf en vertical, medido en milimetros y con un tamaño de A4
    pdf.alias_nb_pages() # Contador de páginas
    pdf.set_margins(30, 25, 30) # Establezco los márgenes
    pdf.set_auto_page_break(auto = True, margin = 30) # Establezco el cambio de página automatico a los tres centimetros del final del folio
    pdf.add_page() # Añado una página
    pdf.portada() # Creo la portada
    # Defino el primer apartado
    texto0 = """A lo largo de este documento se analizarán distintos aspectos sobre el equipo de baloncesto estadounidense 'Brooklyn Nets' en la temporada del año 2022. Este equipo compite en la NBA, en concreto, en la División Atlática de la Conferencia Este de dicha liga, siendo el equipo local cuando juegan en el Barclays Center (barrio de Brooklyn).\n
Este equipo ha ido cambiando su nombre desde su fundación en 1967. Comenzó llamandose 'New Jersey Americans' cuando jugaban en la ABA (1967) y al año siguiente se cambiaron el nombre a 'New York Nets' al mudarse a Nueva York. Continuaron con dicho nombre hasta que, un año más tarde de ingresar en la NBA (1976), volvieron a Nueva Jersey adoptando el nombre de 'New Jersey Nets'. Finalmente, en 2012 pasaron a llamarse 'Brooklyn Nets' al trasladarse a Brooklyn.\n
Los Nets tuvieron  sus últimos grandes éxitos en 2002 y 2003 ganando las finales de la NBA de ambos años. Para poder conseguir de nuevo estos logros, se ofrece un análisis detallado del equipo en la última temporada para saber los puntos fuertes y débiles, y donde ha de mejorar este equipo. """ 
    pdf.imprimo_apartado(0, 'Introducción', texto0)
    
    # Defino el segundo apartado
    texto1 = "En primer lugar, se ofrece un resumen de la plantilla del equipo con sus respectivas imágenes, datos personales y la posición en la que juegan. Para más información, haciendo click en cada imagen, se puede acceder a la página oficial del equipo con información de cada jugador."
    pdf.imprimo_apartado(1, 'Plantilla del equipo', texto1)
    plantilla_jugadores(pdf, caracteristicas_jugador) # Imprimo en el pdf la pantilla llamando a la funcion creada previamente
    pdf.set_font('times', '', 11)
    # Escribo otro párrafo en el mismo apartado
    pdf.multi_cell(0, 5, 'La tabla que se observa a continuación presenta datos personales de cada jugador como la altura y el peso. Esta tabla se encuentra ordenada en el orden de las imagenes anteriores, es decir, en función del número que tienen en su equipación.')
    columnas = list(caracteristicas_jugador.columns)
    columnas.remove('Position')
    df_tabla = caracteristicas_jugador[columnas].copy() # Guardo en un nuevo df los datos que nos interesan para la tabla
    pdf.tabla_basica(df_tabla, None) # Imprimo en el pdf una tabla
    pdf.ln(10)
    # Escribo un nuevo párrafo
    pdf.multi_cell(0, 5, 'A continuación se puede observar la posición en la que juega cada jugador junto a un esquema de las posiciones') 
    # Defino las distintas posiciones en un diccionario con sus repectivas abreviaturas
    posiciones = {'SF': 'Alero', 'PG': 'Base', 'SG': 'Escolta', 'PF': 'Ala-Pivot', 'C': 'Pivot'}
    # Creo una lista con la descripcion de las posiciones
    descripcion = [posiciones[caracteristicas_jugador.loc[fila, 'Position']] for fila in range(len(caracteristicas_jugador))]
    df_posiciones = caracteristicas_jugador[['Name', 'Position']] # Defino el nuevo df con los datos necesarios
    df_posiciones = df_posiciones.rename(columns = {'Position': 'Abbreviation'})
    df_posiciones['Position'] = descripcion 
    pdf.tabla_basica(df_posiciones, None) #vImprimo la tabla en el pdf
    pdf.set_font('times', 'b', 11)
    pdf.ln(10)
    pdf.cell(0, 10, 'Esquema de las distintas posiciones', 0, 0, 'L')
    pdf.ln(15)
    if not os.path.exists('posiciones_basket.jpg'): # Compuebo que la imagen no esté en el directorio indicado
        # Si la imagen no se encuentra entonces guardo la foto
        guardar_foto('posiciones_basket.jpg', "https://www.competize.com/blog/wp-content/uploads/2021/03/posiciones-baloncesto-cancha-escolta-base-alero.jpg")
    pdf.image('posiciones_basket.jpg', w = 100) # La imprimo en el pdf
    
    # Defino el tercer apartado
    texto2 = "En este apartado se realiza un analisis detallado de la temporada por cada jugador, atendiendo a las faltas cometidas por cada uno o los puntos conseguidos. A continuación, se observa una tabla con los distintos datos analizados, además de la suma total del equipo (en la última fila)."
    pdf.imprimo_apartado(2, "Analisis de la temporada por jugador", texto2)
    # Defino el nuevo df con la info general de la temporada
    df_temporada = info_stats[['Name', 'Games', 'Time', 'PersonalFouls','Rebounds', 'Assists', 'Steals', 'BlockedShots', 'Points', 'PlusMinus']]
    pdf.tabla_basica(df_temporada, abreviaturas) # Imprimo en el pdf la tabla
    
    # Defino el cuarto apartado
    texto3 = "En este apartado se realiza un analisis detallado de la temporada por cada jugador en función de los tiros, atendiendo a los tiros libres, triples y tiros de campo. En primer lugar, se observa una tabla con los tiros de campo intentados y marcados según el jugador, además del porcentaje de los encestados con respectos a los tirados por cada uno y la suma total del equipo (en la última fila)."
    pdf.imprimo_apartado(3, "Analisis de los tiros por cada jugador", texto3)
    # Defino el nuevo df con los datos referentes a los tiros de campo ordenados por el numero de tiros encestados
    df_dobles = info_stats[['Name', 'FieldGoalsMade', 'FieldGoalsAttempted', 'FieldGoalsPercentage']].sort_values(by = 'FieldGoalsMade', ascending = False)
    # Creo una ultima fila con la media de todo el equipo
    total = {'Name': 'TOTAL'}
    total.update({col: round(df_dobles.loc[:,col].mean(), 2) for col in list(df_dobles.columns) if col != 'Name'}) 
    df_dobles = df_dobles.append(total, ignore_index = True)
    pdf.tabla_basica(df_dobles, abreviaturas) # Imprimo en el pdf la tabla con los datos
    pdf.ln(5)
    # Escribo un nuevo párrafo
    pdf.multi_cell(150, 6, 'Para analizar de mejor manera la tabla anterior, se puede observar a continuación un gráfico de barras en el que se muestra el número de los tiros de campo marcados respecto al total de los intentados y ordenado de mayor a menor respecto a los tiros encestados.')
    # Creo el df con los datos para el gráfico con los datos de los tiros de campos encestados y los tiros fallados para poder ver el total
    df_dobles_grafico = df_dobles[['Name', 'FieldGoalsMade']]
    df_dobles_grafico['FieldGoalsFailed'] = [df_dobles.loc[fila, 'FieldGoalsAttempted'] - df_dobles.loc[fila, 'FieldGoalsMade'] for fila in range(len(df_dobles))]
    # Creo el gráfico
    crear_grafico_barras_apiladas(df_dobles_grafico.iloc[:-1, :], 'Jugadores', 'Tiros de campo', 'Análisis de los tiros de campo según el jugador', 'tiros_dobles.png')
    pdf.image('tiros_dobles.png', w = 150) # Pego el gráfico en el pdf
    pdf.ln(5)
    
    texto4 = "En segundo lugar se analizan los tiros libres de cada jugador. Para ello, se puede observar una tabla similar a la anterior con los datos de los tiros libres."
    pdf.multi_cell(150, 6, texto4) # Escribo nu nuevo párrafo
    # Defino el nuevo df con los datos referentes a los tiros libres ordenados por el numero de tiros encestados
    df_libres = info_stats[['Name', 'FreeThrowsMade', 'FreeThrowsAttempted', 'FreeThrowsPercentage']].sort_values(by = 'FreeThrowsMade', ascending = False)
    # Creo una ultima fila con la media de todo el equipo
    total2 = {'Name': 'TOTAL'}
    total2.update({col: round(df_libres.loc[:,col].mean(), 2) for col in list(df_libres.columns) if col != 'Name'}) 
    df_libres = df_libres.append(total2, ignore_index = True)
    pdf.tabla_basica(df_libres, abreviaturas) # Imprimo en el pdf la tabla con los datos
    pdf.ln(5)
    # Escribo nu nuevo párrafo
    pdf.multi_cell(150, 6, 'Tras haber analizado los datos de manera numérica, se puede observar los datos de manera visual en un gráfico de barras en el que se muestra el número de los tiros libres marcados respecto al total de los intentados y ordenado de mayor a menor respecto a los tiros encestados.')
    # Creo el df con los datos para el gráfico con los datos de los tiros libres encestados y los tiros fallados para poder ver el total
    df_libres_grafico = df_libres[['Name', 'FreeThrowsMade']]
    df_libres_grafico['FreeThrowsFailed'] = [df_libres.loc[fila, 'FreeThrowsAttempted'] - df_libres.loc[fila, 'FreeThrowsMade'] for fila in range(len(df_libres))] 
    # Creo el gráfico
    crear_grafico_barras_apiladas(df_libres_grafico.iloc[:-1, :], 'Jugadores', 'Tiros libres', 'Análisis de los tiros libres según el jugador', 'tiros_libres.png')
    pdf.image('tiros_libres.png', w = 150) # Pego el gráfico en el pdf
    pdf.ln(5)
    
    texto5 = "Y por último en este apartado se analizan los tiros triples de cada jugador. Para ello, se puede observar una tabla similar a las anteriores de este mismo apartado con los datos de los tiros triples."
    # Escribo nu nuevo párrafo
    pdf.multi_cell(150, 6, texto5)
    # Defino el nuevo df con los datos referentes a los tiros triples ordenados por el numero de tiros encestados
    df_triples = info_stats[['Name', 'ThreePointersMade', 'ThreePointersAttempted', 'ThreePointersPercentage']].sort_values(by = 'ThreePointersMade', ascending = False)
    # Creo una ultima fila con la media de todo el equipo
    total3 = {'Name': 'TOTAL'}
    total3.update({col: round(df_triples.loc[:,col].mean(), 2) for col in list(df_triples.columns) if col != 'Name'}) 
    df_triples = df_triples.append(total3, ignore_index = True)
    pdf.tabla_basica(df_triples, abreviaturas) # Imprimo en el pdf la tabla con los datos
    pdf.ln(5)
    # Escribo un nuevo párrafo
    pdf.multi_cell(150, 6, 'De la misma manera que en los tiros de campo y los tiros libres, se puede observar un gráfico de barras en el que se muestra el número de los tiros triples marcados respecto al total de los intentados y ordenado de mayor a menor respecto a los tiros encestados.')
    # Creo el df con los datos para el gráfico con los datos de los tiros tiples encestados y los tiros fallados para poder ver el total
    df_triples_grafico = df_triples[['Name', 'ThreePointersMade']]
    df_triples_grafico['ThreePointersFailed'] = [df_triples.loc[fila, 'ThreePointersAttempted'] - df_triples.loc[fila, 'ThreePointersMade'] for fila in range(len(df_triples))] 
    # Creo el gráfico
    crear_grafico_barras_apiladas(df_triples_grafico.iloc [:-1, :], 'Jugadores', 'Tiros triples', 'Análisis de los tiros triples según el jugador', 'tiros_triples.png')
    pdf.image('tiros_triples.png', w = 150) # Pego el gráfico en el pdf
    
    # Defino el quinto apartado
    texto6 = "En este apartado se realiza un analisis detallado de la temporada por cada jugador en función de los rebotes, atendiendo a los rebotes ofensivos y los defensivos. A continucación se puede observar una tabla con los rebotes (ofensivos, defensivos y totales), además del porcentaje de cada uno y la suma total del equipo (en la última fila)."
    pdf.imprimo_apartado(4, "Analisis de los rebotes por cada jugador", texto6)
    # Defino un nuevo df con todos los datos de los rebotes
    df_rebotes = info_stats[['Name', 'OffensiveRebounds', 'OffensiveReboundsPercentage', 'DefensiveRebounds','DefensiveReboundsPercentage', 'Rebounds', 'TotalReboundsPercentage']].sort_values(by = 'Rebounds', ascending = False)
    # Creo una ultima fila con la media de todo el equipo
    total4 = {'Name': 'TOTAL'}
    total4.update({col: round(df_rebotes.loc[:,col].mean(), 2) for col in list(df_rebotes.columns) if col != 'Name'}) 
    df_rebotes = df_rebotes.append(total4, ignore_index = True)
    pdf.tabla_basica(df_rebotes, abreviaturas) # Imprimo en el pdf la tabla con los datos
    pdf.ln(5)
    # Escribo un nuevo parrafo
    pdf.multi_cell(150, 6, 'En segundo lugar, se puede observar un gráfico de barras en el que se muestra el número de los rebotes ofensivos realizados por cada uno de los jugadores, y ordenado de mayor a menor.')
    # Creo el df con los datos para el gráfico con los datos de los rebotes ofensivos realizados por cada jugador
    df_rebotes_ofensivos = df_rebotes[['Name', 'OffensiveRebounds']].sort_values(by = 'OffensiveRebounds', ascending = False)
    # Creo el gráfico
    crear_grafico_barras_apiladas(df_rebotes_ofensivos.iloc[:-1, :], 'Jugadores', 'Rebotes ofensivos', 'Análisis de los rebotes ofensivos según el jugador', 'rebotes_ofensivos.png')
    pdf.image('rebotes_ofensivos.png', w = 150) # Pego el grafico en el pdf
    pdf.ln(5)
    # Escribo un nuevo párrafo
    pdf.multi_cell(150, 6, 'Y por último, se puede observar un gráfico de barras en el que se muestra el número de los rebotes ofensivos realizados por cada uno de los jugadores, y ordenado de mayor a menor.')
    # Creo el df con los datos para el gráfico con los datos de los rebotes defensivos realizados por cada jugador
    df_rebotes_defensivos = df_rebotes[['Name', 'DefensiveRebounds']].sort_values(by = 'DefensiveRebounds', ascending = False)
    # Creo el gráfico
    crear_grafico_barras_apiladas(df_rebotes_defensivos.iloc[:-1, :], 'Jugadores', 'Rebotes defensivos', 'Análisis de los rebotes defensivos según el jugador', 'rebotes_defensivos.png')
    pdf.image('rebotes_defensivos.png', w = 150) # Pego el grafico en el pdf
    
    # Defino el sexto apartado
    texto = "En este último apartado podemos observar un glosario sobre las distintas entradas de las tablas que han aparecido a lo largo del documento."
    pdf.imprimo_apartado(5, "Glosario de las tabla", texto)
    # Escribo en el pdf una lista con las distintas abreviaturas y su significado 
    for key in list(abreviaturas.keys()):
        pdf.cell(0,10, f'   - {key}: {abreviaturas[key]}', 0, 0, 'L')
        pdf.ln(5) 
    # Exporto el pdf
    pdf.output('Brooklyn Nets.pdf')
    
if __name__ == "__main__": # Defino el proceso principal con la estructura de ETL
    # Guardo las fotos de los jugadores del equipo si no están guardadas ya en el directorio
    for num_foto in range(len(fotos_equipo)):
        nombre = f"jugador_{num_foto}.png"
        if not os.path.exists(nombre):
            guardar_foto(nombre, fotos_equipo[num_foto])
            
    # Defino la urls de las apis de las que voy a extraer los datos
    url_stats = "https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStatsByTeam/2023/BKN"
    url_players = "https://api.sportsdata.io/v3/nba/scores/json/Players/BKN"
    
    clave = "XXXXXXXXXX"  # Escribo la clave personal de acceso a las api sustituyendolas por las x y sin espacios
    headers = {"Ocp-Apim-Subscription-Key": clave} # Establezco las headers necesarias para acceder a las apis 
    response, response2 = extract(url_stats, url_players, headers) # Extraigo los datos
    caracteristicas_jugador, info_stats = transform(response, response2) # Transformo los datos
    load(info_stats, caracteristicas_jugador) # Cargo los datos en un pdf
