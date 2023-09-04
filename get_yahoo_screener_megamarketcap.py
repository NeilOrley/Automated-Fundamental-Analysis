from yahoofinance_utils import fetch_stock_screener_data_from_yahoo, fetch_stock_statistics_data_from_yahoo, update_existing_dataframe, get_financial_indicators
from tqdm import tqdm
import time
import random
import pandas as pd

# Utilisation de la fonction
url = 'https://query2.finance.yahoo.com/v1/finance/screener?crumb=97mj2bvtrFl&lang=en-US&region=US&formatted=true&corsDomain=finance.yahoo.com'
step = 100
query = '{ "operator": "AND", "operands": [ { "operator": "or", "operands": [ { "operator": "GT", "operands": ["intradaymarketcap", 100000000000 ] } ] } ] }'

# DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
all_quotes = pd.read_csv('all_quotes_from_yahoo.csv') #### DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
#all_quotes = fetch_stock_screener_data_from_yahoo(url, step, query)

symbols = all_quotes['symbol'].unique()
unique_symbols_count = len(symbols)

#with tqdm(total = unique_symbols_count) as pbar:
for symbol in symbols:
    #url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?crumb=.w4kPq%2FeFF0&lang=en-US&region=US&modules=defaultKeyStatistics%2CfinancialData%2CcalendarEvents&corsDomain=finance.yahoo.com'
    #statistics_data = fetch_stock_statistics_data_from_yahoo(url, symbol)
    statistics_data = get_financial_indicators(symbol)
    #all_quotes = update_existing_dataframe(all_quotes, statistics_data, symbol)
      #pbar.update(1)


# Enregistrer le DataFrame dans un fichier CSV
all_quotes.to_csv('all_quotes_from_yahoo_enriched.csv', index=False)