import csv
import ast
import json
import warnings
from tqdm import tqdm
import time
import pandas as pd
import requests
import random
from yahooquery import Ticker


def get_financial_indicators(symbol):

    # Désactivation des warnings
    warnings.filterwarnings('ignore')
    
    ticker = Ticker(symbol, verify=False)

    data = ticker.financial_data 
    data = pd.DataFrame(data).transpose()
    data = data.reset_index(drop=True)


    balance_sheet = ticker.balance_sheet()
    try:
        balance_sheet = balance_sheet.fillna(method='ffill') # Rempli les NaN par la dernière valeur disponible    
        balance_sheet = balance_sheet.drop('asOfDate', axis=1) 
        balance_sheet = balance_sheet.drop('periodType', axis=1) 
        balance_sheet = balance_sheet.drop('currencyCode', axis=1) 
        balance_sheet = balance_sheet.reset_index(drop=True)
        #balance_sheet = balance_sheet.iloc[-1].transpose()
        balance_sheet = pd.DataFrame(balance_sheet).tail(1) 
    except:
        # Gérer le cas où ce n'est pas un DataFrame
        print("Erreur : balance_sheet n'est pas un DataFrame")
        balance_sheet = pd.DataFrame()


    cash_flow = ticker.cash_flow()    
    try:
        cash_flow = cash_flow.fillna(method='ffill') # Rempli les NaN par la dernière valeur disponible
        cash_flow = cash_flow.drop('asOfDate', axis=1) 
        cash_flow = cash_flow.drop('periodType', axis=1) 
        cash_flow = cash_flow.drop('currencyCode', axis=1)   
        cash_flow = cash_flow.reset_index(drop=True)
        #cash_flow = cash_flow.iloc[-1].transpose()
        cash_flow = pd.DataFrame(cash_flow).tail(1) 
    except:
        # Gérer le cas où ce n'est pas un DataFrame
        print("Erreur : cash_flow n'est pas un DataFrame")
        cash_flow = pd.DataFrame()
    

    income_statement = ticker.cash_flow()
    try:
        income_statement = income_statement.fillna(method='ffill') # Rempli les NaN par la dernière valeur disponible
        income_statement = income_statement.drop('asOfDate', axis=1) 
        income_statement = income_statement.drop('periodType', axis=1) 
        income_statement = income_statement.drop('currencyCode', axis=1) 
        income_statement = income_statement.reset_index(drop=True)
        #income_statement = income_statement.iloc[-1].transpose()
        income_statement = pd.DataFrame(income_statement).tail(1)
    except:
        # Gérer le cas où ce n'est pas un DataFrame
        print("Erreur : income_statement n'est pas un DataFrame")
        income_statement = pd.DataFrame()
    

    valuation = ticker.valuation_measures
    try:
        valuation = valuation.fillna(method='ffill') # Rempli les NaN par la dernière valeur disponible
        valuation = valuation.drop('asOfDate', axis=1) 
        valuation = valuation.drop('periodType', axis=1) 
        valuation = valuation.reset_index(drop=True)
        #valuation = valuation.iloc[-1].transpose()
        valuation = pd.DataFrame(valuation).tail(1)
    except:
        # Gérer le cas où ce n'est pas un DataFrame
        print("Erreur : valuation n'est pas un DataFrame")
        valuation = pd.DataFrame()
    

    #sector_trend = ticker.get_modules('sectorTrend')    
    analysis = pd.concat([data, balance_sheet, cash_flow, income_statement, valuation])
    analysis.reset_index(drop=True, inplace=True)
    series = analysis.stack()
    print(series)
    return series


"""
Ces 2 fonctions permettent d'aller l'onglet statistics d'un symbol spécifique sur yahoo finance
/!\ : problème de performance
"""
def extract_data_from_json_for_statistics(data_dict):
    return data_dict['quoteSummary']['result'][0]


def convert_to_dataframe_for_statistics(data):
    raw_data = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    raw_value = sub_value.get("raw", "N/A")
                    raw_data[f"{key}_{sub_key}"] = raw_value
                    
    return pd.Series(raw_data)


def get_headers_for_statistics(symbol):
    return {
        'authority' : 'query1.finance.yahoo.com',
        'accept' : '*/*',
        'accept-language' : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control' : 'no-cache',
        'cookie' : 'EuConsent=CPxRBIAPxRBIAAOACBFRDUCoAP_AAEfAACiQgoNB9G7WTXNncXp_YPs0eYUX1VBp4uAxBgCBA-ABzBsUIIwGVmEzJEyIJigCGAIAoGJBIEFtGAlAQFAQYIAFABHICEEAJBAAIGAAECAAAgBACBBIEwAAAAAQoUBXMhQgkAdEQFoIQchAlgAgAQIAICAEoIhBAgQAEAAgQABICEAIgigAggAAAAIAAAAEAFAIEQBQBgFCB____eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQTFABINSogCbAgJCaQMIoEQIgqCACgUAAAAECBAAAmDAoQRgEqMBkAIEQABAAAAABQEACAAACABCAAIAggQAAACAQAAAAQCAAAEAAAAAAAAAAAAAQAgAAAAAAQgCIQAhBAACAACAAgoAAIABAAAAAAEAIARCAAAAAAABAAAAAAIAQBAABAAAAAAQAAAAAAAAQIACADAAADgkbLUAMNABgACIKAiADAAEQUBUAGAAIgoA; A1=d=AQABBDIK7mQCEN9DuofoZi_AJ9MmnmXdvzsFEgABCAFS72QfZeUzb2UB9qMAAAcIIwruZHvyFo4&S=AQAAAog8H4dshHfNDGZ_XsXy89Q; A3=d=AQABBDIK7mQCEN9DuofoZi_AJ9MmnmXdvzsFEgABCAFS72QfZeUzb2UB9qMAAAcIIwruZHvyFo4&S=AQAAAog8H4dshHfNDGZ_XsXy89Q; GUC=AQABCAFk71JlH0IgTQSQ&s=AQAAAHg4UO7g&g=ZO4KPA; PRF=t%3DTM.BA%252BMNSO%252BLGHL%252BPRDO%252BTKC%252BAAPL%252BAAPL.MX%252B%255EGSPC%252B%255EMXX%252BES%253DF%252B1320.T%252B6825.TWO%26newChartbetateaser%3D1; A1S=d=AQABBDIK7mQCEN9DuofoZi_AJ9MmnmXdvzsFEgABCAFS72QfZeUzb2UB9qMAAAcIIwruZHvyFo4&S=AQAAAog8H4dshHfNDGZ_XsXy89Q&j=GDPR; cmp=t=1693569890&j=1&u=1---&v=93',
        'origin' : 'https://finance.yahoo.com',
        'pragma' : 'no-cache',
        'referer' : 'https://finance.yahoo.com/quote/TM.BA/press-releases?p='+str(symbol),
        'sec-ch-ua' : '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile' : '?0',
        'sec-ch-ua-platform' : '"Windows"',
        'sec-fetch-dest' : 'empty',
        'sec-fetch-mode' : 'cors',
        'sec-fetch-site' : 'same-site',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

def fetch_stock_statistics_data_from_yahoo(url, symbol):
    # Désactivation des warnings
    warnings.filterwarnings('ignore')

    response = json.loads(requests.get(url, verify=False, headers=get_headers_for_statistics(symbol), data='', timeout=30).content)

    # Extraire les données spécifiques
    result_data = extract_data_from_json_for_statistics(response)
    
    # Convertir les données en DataFrame
    new_data_series = convert_to_dataframe_for_statistics(result_data)

    return new_data_series

"""
Ces 3 fonctions permettent d'aller récupérer un screener particulier sur yahoo finance
"""
def get_headers_for_screener(offset):
    return {
        'authority': 'query2.finance.yahoo.com',
        'accept': '*/*',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type' : 'application/json',
        'cookie' : 'cmp=t=1693295706&j=1&u=1---&v=93; PRF=t%3D005930.KS%252BHPG.VN%252BIBP%252BCROX%252BAMWD%252BTGNA%252BPERI%252BUSLM%252BLTHM%252BEXP%252BLIZI%252BUAN%252BSSL%252BDRD%252BAMR%26newChartbetateaser%3D1; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiQzRGVkdHWktKS1JBTDJRTU5YTEpCWVhPRkEiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiIzaWtncFp2dURCNjYifX0.CxMDu77mL_Z-FVMWMiQHrTLvafGwfArnb9cSIyr9HSx1YMb0Xg_2NI4Ag6aAHX0ZKHDRBvRkVW8yrtJRFfWY5IDdY6S-hF8O_oEkXovUnRk5HWb3YovH56j3ib4QIGWUeTMRnbiNfdLZLa8mYJ-GGZkseRvUR4AbS1Gt4Pwe6QY; T=af=JnRzPTE2OTMyOTYzNDkmcHM9SW5POTllakU5R3QzeW8zeER3dFBHUS0t&d=bnMBeWFob28BZwFDNEZWR0daS0pLUkFMMlFNTlhMSkJZWE9GQQFhYwFBR2dWM3VZNQFhbAFuZWlsb3JsZXlAZ21haWwuY29tAXNjAW1icl9yZWdpc3RyYXRpb24BZnMBNUIyTkh4NWs3YWJkAXp6AWRiYTdrQkE3RQFhAVFBRQFsYXQBZGJhN2tCAW51ATA-&kt=EAAFn4HOqjbgbvfaJzyajCKNg--~I&ku=FAAEg4IHW2Ah7Te349LbGiJQZ93B_QyDdwZzNDagk8WpcsaPW5mohfGeOFqKgLxDvtnUu66wlZW7iEfkNTmN2vOtn22nfK.w_gUpZ_FjAWoz_PWxqEhejUV2Za061uyD.bqTA_pFwlXHyxNrEfWF8OeTrcL7MHX5_8O2vQMgnqolCQ-~E; F=d=Xoa8ILg9vMe5UB63L8FPzPpVbPQCIW.RKfseox1U.4d3py4yDNZv; PH=l=fr-FR; Y=v=1&n=71qc46nmg3q2t&l=gkf6id6cwjdbwk5whstif7cl4155oh3j2c00c1gp/o&p=n2hvvfr00000000&r=1c9&intl=fr; GUCS=ATqwr8Qe; EuConsent=CPxRBIAPxRBIAAOACBFRDUCoAP_AAEfAACiQgoNB9G7WTXNncXp_YPs0eYUX1VBp4uAxBgCBA-ABzBsUIIwGVmEzJEyIJigCGAIAoGJBIEFtGAlAQFAQYIAFABHICEEAJBAAIGAAECAAAgBACBBIEwAAAAAQoUBXMhQgkAdEQFoIQchAlgAgAQIAICAEoIhBAgQAEAAgQABICEAIgigAggAAAAIAAAAEAFAIEQBQBgFCB____eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQTFABINSogCbAgJCaQMIoEQIgqCACgUAAAAECBAAAmDAoQRgEqMBkAIEQABAAAAABQEACAAACABCAAIAggQAAACAQAAAAQCAAAEAAAAAAAAAAAAAQAgAAAAAAQgCIQAhBAACAACAAgoAAIABAAAAAAEAIARCAAAAAAABAAAAAAIAQBAABAAAAAAQAAAAAAAAQIACADAAADgkbLUAMNABgACIKAiADAAEQUBUAGAAIgoA; GUC=AQABCAFk7vhlIkIetwS3&s=AQAAAOEb3Yly&g=ZO2m7w; A1=d=AQABBOWm7WQCEAJD8AN_UmSU0oEI84IOUCYFEgABCAH47mQiZeUzb2UB9qMAAAcIM_7VZJwAWFoIDxPa-R77LB4yXDZCi1WEyAkBBw&S=AQAAAhQu0PsfQ0q3AYTVyG04-Ms; A3=d=AQABBOWm7WQCEAJD8AN_UmSU0oEI84IOUCYFEgABCAH47mQiZeUzb2UB9qMAAAcIM_7VZJwAWFoIDxPa-R77LB4yXDZCi1WEyAkBBw&S=AQAAAhQu0PsfQ0q3AYTVyG04-Ms; A1S=d=AQABBOWm7WQCEAJD8AN_UmSU0oEI84IOUCYFEgABCAH47mQiZeUzb2UB9qMAAAcIM_7VZJwAWFoIDxPa-R77LB4yXDZCi1WEyAkBBw&S=AQAAAhQu0PsfQ0q3AYTVyG04-Ms&j=GDPR',
        'origin': 'https://finance.yahoo.com',
        'pragma': 'no-cache',
        'referer': 'https://finance.yahoo.com/screener/79a1ce37-1642-47f7-8b7f-f0149304c562?offset='+str(offset)+'&count=100',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }


def get_data_for_screener(offset=0, query=""):
    data = json.loads('{\
                        "size": 100,\
                        "offset": '+str(offset)+',\
                        "sortField": "intradaymarketcap",\
                        "sortType": "DESC",\
                        "quoteType": "EQUITY",\
                        "topOperator": "AND",\
                        "query": '+str(query)+',\
                        "userId": "C4FVGGZKJKRAL2QMNXLJBYXOFA",\
                        "userIdType": "guid"\
                        }')
    return data

def fetch_stock_screener_data_from_yahoo(url, step=100, query=""):
    # Désactivation des warnings
    warnings.filterwarnings('ignore')

    # Créer une liste pour stocker les DataFrames
    dfs = []

    # Premier appel pour obtenir le total des stocks
    response = json.loads(requests.post(url, verify=False, headers=get_headers_for_screener(0), data=json.dumps(get_data_for_screener(offset=0, query=query)), timeout=30).content)
    quotes = response.get('finance', {}).get('result', [{}])[0].get('quotes', [])
    dfs.append(pd.DataFrame(quotes))

    total_value = response.get('finance', {}).get('result', [{}])[0].get('total', None)
    if total_value is not None:
        total_value = int(total_value) + 1
    else:
        total_value = 100

    if total_value > 9900:
        print("WARNING : Il y a trop de ticker a récupérer. L'API Yahoo ne répondra plus a partir de 9900.")

    print('\nScraping data from Yahoo...\n')
    print('\nTotal Stocks:', total_value)

    with tqdm(total = total_value) as pbar:
        # Récupère les données d'un screener particulier
        for offset in range(100, total_value, step):
            try:
                response = json.loads(requests.post(url, verify=False, headers=get_headers_for_screener(offset), data=json.dumps(get_data_for_screener(offset=offset, query=query)), timeout=30).content)
                quotes = response.get('finance', {}).get('result', [{}])[0].get('quotes', [])
                dfs.append(pd.DataFrame(quotes))
            except Exception as e:
                print(f"Erreur lors de la récupération des données à l'offset {offset}: {e}")

            pbar.update(step)
            random_number = random.uniform(0.25, 0.5)
            time.sleep(random_number)

    ## Concaténer tous les DataFrames en un seul et dump dans un CSV
    df_all_quotes = pd.concat(dfs, ignore_index=True)
    # Supprimer les doublons basés sur une colonne spécifique
    df_all_quotes = df_all_quotes.drop_duplicates(subset=['symbol'])

    # Enregistrer le DataFrame dans un fichier CSV
    df_all_quotes.to_csv('all_quotes_from_yahoo.csv', index=False)

    return df_all_quotes


"""
Cette fonction permet d'ajouter des colones dans un dataframe existant sur une ligne particulière
"""
def update_existing_dataframe(existing_df, new_data_series, symbol):
    # Trouver l'index de la ligne pour le symbole spécifié
    index_to_update = existing_df[existing_df['symbol'] == symbol].index[0]
    
    # Mettre à jour les données pour le symbole spécifié
    for col in new_data_series.index:
        if col not in existing_df.columns:
            existing_df[col] = None
        existing_df.loc[index_to_update, col] = new_data_series[col]
    
    return existing_df



"""
Cette fonction va extraire la valeur de "raw" lorsque les cellules ont ce format : {'raw': X, 'fmt': 'Y'}

"""
def get_raw_value(cell):
    try:
        cell_dict = ast.literal_eval(cell)
        if isinstance(cell_dict, dict) and 'raw' in cell_dict:
            return cell_dict['raw']
        else:
            return cell_dict
    except (ValueError, SyntaxError):
        return cell

"""
Cette fonction lit un fichier CSV généré à partir des données de Yahoo Screener : get_yahooscreener.py et le formate :
 - extrait les valeurs raw
 - filtre les colonnes a conserver
"""
def read_and_modify_csv(input_filename, output_filename, columns_to_keep):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        headers = next(reader)
        
        # Filter headers and find indexes of columns to keep
        filtered_headers = [col for col in headers if col in columns_to_keep]
        filtered_indexes = [headers.index(col) for col in filtered_headers]
        
        writer.writerow(filtered_headers)
        
        all_rows = []
        
        for row in reader:
            modified_row = [get_raw_value(row[i]) for i in filtered_indexes]
            writer.writerow(modified_row)
            all_rows.append(modified_row)
            
    return filtered_headers, all_rows


def test_multiply(headers, all_rows):
    new_header = headers + ["Multiplication"]
    new_rows = []
    for row in all_rows:
        try:
            # Vérifie si les valeurs peuvent être converties en float
            value1 = float(row[1]) if row[1] != '' else 0.0
            value2 = float(row[3]) if row[3] != '' else 0.0
            new_value = value1 * value2
        except ValueError:
            new_value = 'N/A'  # Utilisez une valeur par défaut si la conversion échoue

        new_row = row + [new_value]
        new_rows.append(new_row)

    return new_header, new_rows

def enrich_csv(headers, all_rows, enriched_filename):
    
    new_header, new_rows = test_multiply(headers, all_rows)
    
    with open(enriched_filename, 'w', encoding='utf-8', newline='') as enrichedfile:
        writer = csv.writer(enrichedfile)
        writer.writerow(new_header)
        writer.writerows(new_rows)

    return new_header


"""
Cette fonction trie un fichier CSV en fonction d'un nom de colonne
"""
def sort_and_write_csv(headers, all_rows, sorted_filename, column_name):
    sort_column_index = headers.index(column_name)
    sorted_rows = sorted(all_rows, key=lambda x: x[sort_column_index])
    
    with open(sorted_filename, 'w', encoding='utf-8', newline='') as sortedfile:
        writer = csv.writer(sortedfile)
        writer.writerow(headers)
        writer.writerows(sorted_rows)










""" DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
Fonction de debug pour organiser les différentes étapes en appelant les fonctions en séquence.
"""
def main():
    input_filename = 'data.csv'
    output_filename = 'modified_data.csv'
    enriched_filename = 'enriched_data.csv'
    sorted_filename = 'sorted_data.csv'
    column_name_to_sort = 'symbol'  # Replace this with the actual column name
    
    columns_to_keep = ['symbol','twoHundredDayAverageChangePercent','averageAnalystRating',
                       'fiftyTwoWeekLowChangePercent','language','dividendYield','regularMarketDayRange',
                       'earningsTimestampEnd','epsForward','regularMarketDayHigh','twoHundredDayAverageChange',
                       'twoHundredDayAverage','askSize','bookValue','marketCap','fiftyTwoWeekHighChange',
                       'fiftyTwoWeekRange','fiftyDayAverageChange','exchangeDataDelayedBy',
                       'averageDailyVolume3Month','firstTradeDateMilliseconds','dividendRate',
                       'fiftyTwoWeekChangePercent','trailingAnnualDividendRate','fiftyTwoWeekLow','regularMarketVolume',
                       'market','quoteSourceName','messageBoardId','priceHint','regularMarketDayLow','sourceInterval',
                       'exchange','shortName','region','fiftyDayAverageChangePercent','fullExchangeName',
                       'earningsTimestampStart','financialCurrency','gmtOffSetMilliseconds','regularMarketOpen',
                       'regularMarketTime','regularMarketChangePercent','trailingAnnualDividendYield','quoteType',
                       'averageDailyVolume10Day','fiftyTwoWeekLowChange','fiftyTwoWeekHighChangePercent','typeDisp',
                       'trailingPE','tradeable','currency','sharesOutstanding','regularMarketPreviousClose',
                       'fiftyTwoWeekHigh','exchangeTimezoneName','regularMarketChange','bidSize','priceEpsCurrentYear',
                       'cryptoTradeable','fiftyDayAverage','exchangeTimezoneShortName','epsCurrentYear','customPriceAlertConfidence',
                       'regularMarketPrice','marketState','forwardPE','earningsTimestamp','ask','epsTrailingTwelveMonths',
                       'bid','triggerable','priceToBook','longName','prevName','nameChangeDate','ipoExpectedDate',
                       'dividendDate','openInterest','preMarketChangePercent','preMarketTime','displayName',
                       'preMarketPrice','preMarketChange','underlyingSymbol','newListingDate','exchangeTransferDate','prevExchange']  # Replace with actual columns you want to keep
    
    headers, all_rows = read_and_modify_csv(input_filename, output_filename, columns_to_keep)
    enriched_headers = enrich_csv(headers, all_rows, enriched_filename)
    sort_and_write_csv(enriched_headers, all_rows, sorted_filename, column_name_to_sort)

if __name__ == "__main__":
    main()
