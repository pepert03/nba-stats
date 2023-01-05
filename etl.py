import re
import requests
import pandas as pd
import bs4
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # que la primera pagina no tenga header ni footer:
        if self.page_no() == 1:
            return
        if self.page_no() == 2:
            self.set_font('Helvetica', 'B', 15)
            self.cell(50)
            self.cell(90, 10, 'Standings 2022', 1, 0, 'C')
            self.ln(20)
            self.image('logo.png', 25, 8, 15)
        if self.page_no() == 3:
            self.set_font('Helvetica', 'B', 15)
            self.cell(50)
            self.cell(90, 10, 'Players Chicago Bulls', 1, 0, 'C')
            self.ln(20)
            self.image('logo.png', 25, 8, 15)
        if self.page_no() == 4:
            self.set_font('Helvetica', 'B', 15)
            self.cell(50)
            self.cell(90, 10, 'Next game', 1, 0, 'C')
            self.ln(20)



    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def get_data_api():
    url = 'https://api.sportsdata.io/v3/nba/scores/json/Standings/2022'
    with open('config.txt', 'r') as f:
        headers = {'Ocp-Apim-Subscription-Key': f.read()}
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    df = pd.DataFrame(data)
    df = df.rename(columns={'City': 'city', 'Name': 'name','Conference': '   E/W', 'Percentage': 'Percent','HomeWins': 'HomeW', 'HomeLosses': 'HomeL', 'AwayWins': 'AwayW', 'AwayLosses': 'AwayL', 'PointsPerGameFor': '  PPG', 'PointsPerGameAgainst': 'PPGA', 'GamesBack': '  GB', 'ConferenceRank': 'C_Rank'})
    df['Team'] = df['city'] + ' ' + df['name']
    df = df[['Team','   E/W', 'Wins', 'Losses', 'Percent', 'HomeW', 'HomeL', 'AwayW', 'AwayL', '  PPG', 'PPGA', '  GB', 'C_Rank']]
    return df

def get_data_api2():
    team = 'CHI'
    url = 'https://api.sportsdata.io/v3/nba/scores/json/Players/' + team
    with open('config.txt', 'r') as f:
        headers = {'Ocp-Apim-Subscription-Key': f.read()}

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    df = pd.DataFrame(data)
    df = df[['FirstName', 'LastName', 'Position', 'Jersey', 'Height', 'Weight', 'Salary', 'BirthDate', 'BirthState', 'BirthCountry', 'Experience']]
    df['Name'] = df['FirstName'] + ' ' + df['LastName']
    df = df[['Name', 'Position', 'Jersey', 'Height', 'Weight', 'Salary', 'BirthDate', 'BirthState', 'BirthCountry', 'Experience']]
    df = df.rename(columns={'Name': 'Player', 'Position': 'Pos', 'Jersey': 'No.', 'Height': 'Ht.', 'Weight': 'Wt.', 'Salary': 'Salary', 'BirthDate': 'Birth', 'BirthState': 'State', 'BirthCountry': 'Country', 'Experience': 'Exp.'})
    df['Birth'] = df['Birth'].str.split('T').str[0]
    return df


def get_data_scraping():
    team = 'Bulls'
    url = 'https://www.solobasket.com/apuestas-deportivas/pronosticos-nba/'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    partido = soup.find('p', text=re.compile(team))
    if partido:
        a = partido.text
        pronostico = partido.find_next('b').text
    else:
        a = 'No hay partido'
        pronostico = 'No hay pronostico'
    return a, pronostico

    
def to_pdf(df1, df2, partido, pronostico):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 130, 'Chicago Bulls', 0, 0, 'C')
    pdf.ln(20)
    pdf.set_font('Helvetica', 'B', 15)
    pdf.cell(0, 110, 'Season 2022', 0, 0, 'C')
    pdf.image('logo.png', 70, 80, 70)
    

    pdf.ln(20)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(45, 10, str(df1.columns[0]), 1, 0, 'C')
    for i in range(1,len(df1.columns)):
        pdf.cell(12, 10, str(df1.columns[i]), 1, 0, 'C')
    pdf.ln()
    pdf.set_font('Helvetica', '', 8)
    for i in range(len(df1)):
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(45, 7.5, str(df1.iloc[i,0]), 1, 0, 'C')
        pdf.set_font('Helvetica', '', 8)
        for j in range(1,len(df1.columns)):
            pdf.cell(12, 7.5, str(df1.iloc[i,j]), 1, 0, 'C')
        pdf.ln()

    pdf.ln(30)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(45, 10, str(df2.columns[0]), 1, 0, 'C')
    for i in range(1,len(df2.columns)):
        if i == 5 or i == 6 or i == 8:
            pdf.cell(20, 10, str(df2.columns[i]), 1, 0, 'C')
        else:
            pdf.cell(14, 10, str(df2.columns[i]), 1, 0, 'C')
    pdf.ln()
    pdf.set_font('Helvetica', '', 9)
    for i in range(len(df2)):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(45, 12, str(df2.iloc[i,0]), 1, 0, 'C')
        pdf.set_font('Helvetica', '', 9)
        for j in range(1,len(df2.columns)):
            if j == 5 or j == 6 or j == 8:
                pdf.cell(20, 12, str(df2.iloc[i,j]), 1, 0, 'C')
            else:
                pdf.cell(14, 12, str(df2.iloc[i,j]), 1, 0, 'C')
        pdf.ln()

    pdf.ln(60)
    pdf.set_font('Helvetica', 'B', 15)
    pdf.cell(150, 20, 'SIGUIENTE PARTIDO', 1, 0, 'C', center=True)
    pdf.ln()
    pdf.cell(150, 20, partido, 1, 0, 'C', center=True)
    pdf.ln()
    pdf.cell(150, 20, 'PRONOSTICO', 1, 0, 'C', center=True)
    pdf.ln()
    pdf.cell(150, 20, pronostico, 1, 0, 'C', center=True)
    pdf.ln()

    pdf.output('nba_stats.pdf', 'F')


if __name__ == '__main__':
    df1 = get_data_api()
    df2 = get_data_api2()
    partido,pronostico = get_data_scraping()
    to_pdf(df1, df2, partido, pronostico)

