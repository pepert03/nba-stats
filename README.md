nba-stats
=================

## Introducción
Instalar librerías de Python para el análisis de datos:
```
pip install -r requirements.txt
```
Se require una Api-key para [sportsdata](https://api.sportsdata.io/v3/nba/) para poder ejecutar el programa.
Se deberá escribir la api-key en el archivo `config.txt`, y eso es todo lo necesario para ejecutar el programa.

## Ejecución
El archivo `etl.py` es el encargado de realizar la extracción, transformación y carga de los datos. Contiene las siguientes funciones:
- `get_data_api()`: Descarga los datos de la API de todos los equipos de la NBA.
- `get_data_api2()`: Descarga los datos de la API de un equipo en particular( en este caso los Bulls)
- `get_data_scraping()`: Descarga los pronosticos de los partidos de la NBA de la página [SoloBasket](https://www.solobasket.com/apuestas-deportivas/pronosticos-nba/).
- `to_pdf()`: Crea tablas y las guarda en un archivo pdf `nba_stats.pdf`.
