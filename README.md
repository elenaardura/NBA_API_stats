# NBA_API_stats
Este repositorio contiene un programa que obtiene los datos de la temporada de un equipo de la NBA y escribe en un pdf los datos relevantes. Además, contiene un programa que predice el resultado del próximo partido de dicho equipo basándose en la cuota de los equipos que van a disputar el partido, y lo muestra por pantalla. En concreto, el equipo elegido es 'Brooklyn Nets'

El repositorio contiene:
- Un archivo requirements.txt necesario instalarlo antes de llevar a cabo el programa
- Un archivo config.txt para configurar las API
- Un archivo NBA nextmatch_webscrapping.py que es el programa de la prediccion del siguiente partido 
- Un archivo NBA_stats_api.py que es el programa que escribe un pdf con la informacion del equipo indicado de la ultima temporada

Modo de ejecución:
1. Desde la terminal instalar el archivo requirements.txt
2. En el archivo NBA_stats_api.py, en el proceso principal cambiar la clave de acceso a la API, en la linea indicada en el archivo config.txt
3. Ejecutar ambos archivos

En el caso de querer cambiar el equipo para la prediccion de los próximos partidos, en el archivo NBA nextmatch_webcrapping.py, cambiar el nombre en la variable global  EQUIPO.

La API utilizada es la siguiente: https://sportsdata.io/
La web utilizada para realizar el webscrapping y obtener la prediccion es la siguiente: https://www.sportytrader.es/
