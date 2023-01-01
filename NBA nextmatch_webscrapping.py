# Importo las librerias necesarias para llevar a cabo el programa
import requests
import warnings
import sys
import signal
from bs4 import BeautifulSoup

EQUIPO = 'Brooklyn Nets' # Defino el equipo del que vamos a predecir el ganador del proximo partido

def handler_signal(signal, frame): # Creo una función que controle la salida del ctrl + c 
    print('[!] Cerrando el programa...')
    sys.exit()

signal.signal(signal.SIGINT, handler_signal)
warnings.filterwarnings('ignore') # Elimino los avisos de la terminal

def extract(): # Defino la funcion que extrae los datos
    # Establezco la url de la que voy a obtener los datos
    url = "https://www.sportytrader.com/en/odds/basketball/usa/nba-306/" 
    response = requests.get(url) # Extraigo los datos
    return response

def transform(response): # Defino la función que transforma los datos de la forma que quiero 
    html = BeautifulSoup(response.content, 'html.parser') # Creo la sopa con el código fuente de la página en html
    # Busco todos los fututos partidos de la nba
    futuros_partidos = html.find_all('div', {'class': "cursor-pointer border rounded-md mb-4 px-1 py-2 flex flex-col lg:flex-row relative"})
    partidos = []
    for partido in futuros_partidos:
        prediccion = {}
        # De los fututos partidos que va a jugar el equipo seleccionado guardo el día, la hora, que equipos se efrentan en el partido y las cuotas establecidas por la web, 
        # además de la prediccion del ganador en base a la menor cuota
        if EQUIPO in partido.text:
            prediccion['fecha-hora'] = partido.find('span', {'class': "text-sm text-gray-600 w-full lg:w-1/2 text-center dark:text-white"}).text.split(' - ')
            prediccion['equipos'] = partido.find('a', {'class':''}).text[1:-1].split(' - ')
            cuotas =  partido.find_all('span', {'class': "px-1 h-booklogosm font-bold bg-primary-yellow text-white leading-8 rounded-r-md w-14 md:w-18 flex justify-center items-center text-base"})
            prediccion['cuotas'] = [cuota.text for cuota in cuotas]
            partidos.append(prediccion)
            prediccion['ganador'] = prediccion['equipos'][prediccion['cuotas'].index(min(prediccion['cuotas']))]
    return partidos

def load(predicciones): # Defino la funcion que carga los datos al cliente, es decir, se muestra por partalla los fututos partidos del equipo seleccionado junto con la prediccion del ganador
    print(f'\n\nA continuación se muestra la predicción realizada para los próximos partidos del equipo {EQUIPO} basandose en las cuotas de cada equipo.')
    for prediccion in predicciones:
        print(f'\nEl partido que se disputa el día {prediccion["fecha-hora"][0]} a las {prediccion["fecha-hora"][1]} horas entre los equipos:', 
        f'{prediccion["equipos"][0]} y {prediccion["equipos"][1]}, será ganado por el equipo: {prediccion["ganador"]}')
        print(f'Esta predicción se debe a que las cuotas de cada equipo, respectivamente, son las siguientes: {prediccion["cuotas"][0]} y {prediccion["cuotas"][1]}')
    print()

if __name__ == "__main__": # Defino el proceso principal del programa con la estructura de ETL
    response = extract() # Extraigo los datos
    predicciones = transform(response) # Transformo los datos
    load(predicciones) # Cargo los datos al cliente 