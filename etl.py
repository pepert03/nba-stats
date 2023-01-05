'''
Práctica tema 5, Api y web scraping:

-        Senior data analyst de la NBA.

Como senior data analyst, uno de los GM más innovadores de la NBA ha decidido evaluar como se va a comportar su equipo durante los partidos de este año. Por lo que necesitaría construir un analizador de las principales estadísticas del equipo hasta el momento para la temporada 2022-2023 y un pronóstico para el próximo partido. Para ello debes de disponer de una ETL que extraiga, transforme los datos y guarde un informe de los puntos clave del equipo en cuestión en formato pdf y ofrezca por pantalla la predicción para el próximo partido. Entregando el siguiente contenido en el repositorio de datos:

o   Código de una ETL que extraiga datos de una API de datos de la NBA, a continuación, se dejan un par de ejemplos de API:

https://www.api-basketball.com/

https://sportsdata.io/

o   Además  una ETL que obtenga datos usando técnicas de web scraping donde se tendrá que elegir una fuente de datos para obtener pronósticos, como por ejemplo:

https://www.sportytrader.es/

https://www.solobasket.com/apuestas-deportivas/pronosticos-nba/

o   Fichero requirements.txt para la instalación de los recursos necesarios

o   Fichero de config.txt para la configuración necesaria de las ETLs (como por ejemplo los credenciales usados para consumir las APIs, recordar no subir vuestras credenciales, solo el fichero con la estructura necesaria)

o   README.md con la descripción general del repo y las instrucciones de uso.
'''

# Import libraries
import requests
import json
import pandas as pd
import numpy as np
import bs4
import urllib.request
import os

from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(50)
        self.cell(90, 10, 'NBA Team Report', 1, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def get_data_api():
    url = 'https://api.sportsdata.io/v3/nba/scores/json/Standings/2022'
    # api key = c7c28f449c444a89a2d7e3b1bf9b82d1
    headers = {
        'Ocp-Apim-Subscription-Key': 'c7c28f449c444a89a2d7e3b1bf9b82d1'
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    df = pd.DataFrame(data)
    '''
    columnas = 
        Index(['Season', 'SeasonType', 'TeamID', 'Key', 'City', 'Name', 'Conference',
       'Division', 'Wins', 'Losses', 'Percentage', 'ConferenceWins',
       'ConferenceLosses', 'DivisionWins', 'DivisionLosses', 'HomeWins',
       'HomeLosses', 'AwayWins', 'AwayLosses', 'LastTenWins', 'LastTenLosses',
       'PointsPerGameFor', 'PointsPerGameAgainst', 'Streak', 'GamesBack',
       'StreakDescription', 'GlobalTeamID', 'ConferenceRank', 'DivisionRank'],
      dtype='object')
    '''
    # cambiar nombre de columnas:
    df = df.rename(columns={'City': 'city', 'Name': 'name','Conference': '   E/W', 'Percentage': 'Percent','HomeWins': 'HomeW', 'HomeLosses': 'HomeL', 'AwayWins': 'AwayW', 'AwayLosses': 'AwayL', 'PointsPerGameFor': '  PPG', 'PointsPerGameAgainst': 'PPGA', 'GamesBack': '  GB', 'ConferenceRank': 'C_Rank'})
    df['Team'] = df['city'] + ' ' + df['name']
    df = df[['Team','   E/W', 'Wins', 'Losses', 'Percent', 'HomeW', 'HomeL', 'AwayW', 'AwayL', '  PPG', 'PPGA', '  GB', 'C_Rank']]
    # pdf with data table:
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(45, 10, str(df.columns[0]), 1, 0, 'C')
    for i in range(1,len(df.columns)):
        pdf.cell(12, 10, str(df.columns[i]), 1, 0, 'C')
    pdf.ln()
    pdf.set_font('Helvetica', '', 8)
    for i in range(len(df)):
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(45, 7.5, str(df.iloc[i,0]), 1, 0, 'C')
        pdf.set_font('Helvetica', '', 8)
        for j in range(1,len(df.columns)):
            pdf.cell(12, 7.5, str(df.iloc[i,j]), 1, 0, 'C')
        pdf.ln()
    

    pdf.output('nba_stats.pdf', 'F')

get_data_api()

