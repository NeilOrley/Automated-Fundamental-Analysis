import warnings
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os.path
from constants import URL, userAgentList, dataframes, allStockData
from tqdm import tqdm   
import numpy as np

# Désactivation des warnings
warnings.filterwarnings('ignore')

# Récupération du nombre de lignes/stocks à scraper
def getNumStocks(url):

    agent = random.choice(userAgentList)
    headers = {'User-Agent': agent}

    page = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')

    tableRows = soup.find_all('a', class_ = 'screener-link')
    
    raw_num = str(tableRows[0])
    num_stocks = raw_num[raw_num.find('">') + 2 : raw_num.find('</a>')]
    
    return float(num_stocks)

# Scrape des données de la page et stockage dans des dataframes
def get_company_data(url, debug=False):
    
    #global allStockData
    
    # Vérifier si le fichier CSV existe
    csv_filename = f"StockRatings.csv"            

    if os.path.exists(csv_filename) and debug == True:
        # Lire les données depuis le fichier CSV
        allStockData = pd.read_csv(csv_filename)
    else:
        pageCounter = 1
        num_stocks = getNumStocks(f"{URL}&r=10000") if debug == False else 200
        
        print('\nTotal Stocks:', num_stocks)
        print('\nScraping data...\n')

        with tqdm(total = num_stocks) as pbar:
            
            while pageCounter < num_stocks:
                agent = random.choice(userAgentList)
                headers = {'User-Agent': agent}

                page = requests.get(f"{url}&r={pageCounter}", headers=headers, verify=False)
                
                try:
                    tables = pd.read_html(page.text)
                except:
                    soup = BeautifulSoup(page.text, 'html.parser')
                    print('PARSE ERRORR', soup)
                
                try:    
                    table = tables[-2]  
                    
                    if pageCounter != 1:
                        table = table[1:]
                    
                    #print(tables[-2])
                    dataframes.append(table)
                
                except:
                    # print('TABLE ERROR', tables)
                    # print(f"{url}&r={pageCounter}")
                    # print()
                    pass
                    
                pageCounter += 20

                time.sleep(np.random.uniform(0.5, 1))
                
                pbar.update(20)

        allStockData = pd.concat(dataframes)
        allStockData.columns = list(allStockData.iloc[0])
        allStockData = allStockData[1:]
        allStockData.to_csv(csv_filename, index=False)
    
    return allStockData
    