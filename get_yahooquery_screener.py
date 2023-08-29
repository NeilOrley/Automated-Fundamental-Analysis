
import requests
import json
import time
import pandas as pd
import warnings
from tqdm import tqdm   

# Nécessite d'ouvrir Yahoo Query dans un nav et d'avoir un coooki actif
# Open Developer Tools in GoogleChrome (View -> Developer -> Developer Tools).
# Open https://finance.yahoo.com/gainers and configure the filter and click to "Find Stocks"
# After search in Developer Tools you need find page which begin like: screener?crumb
# Click right button then Copy -> Copy as cURL (bash)
# Récupérer les headers

# Désactivation des warnings
warnings.filterwarnings('ignore')

url='https://query2.finance.yahoo.com/v1/finance/screener?crumb=97mj2bvtrFl&lang=en-US&region=US&formatted=true&corsDomain=finance.yahoo.com'
step=100


def get_headers(offset):
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



def get_data(offset=0, query=""):
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


# Créer une liste pour stocker les DataFrames
dfs = []


## Scraping de ticker  
query='{\
  "operator": "AND",\
  "operands": [\
    {\
      "operator": "gt",\
      "operands": [\
        "avgdailyvol3m",\
        100000\
      ]\
    },\
    {\
      "operator": "gt",\
      "operands": [\
        "lastclosemarketcap.lasttwelvemonths",\
        10000000000\
      ]\
    }\
  ]\
}'
response = json.loads(requests.post(url, verify=False, headers=get_headers(0), data=json.dumps(get_data(offset=0, query=query)), timeout=30).content)
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
    for offset in range(100, total_value, step):
        try:
            response = json.loads(requests.post(url, verify=False, headers=get_headers(offset), data=json.dumps(get_data(offset=offset, query=query)), timeout=30).content)
            quotes = response.get('finance', {}).get('result', [{}])[0].get('quotes', [])
            dfs.append(pd.DataFrame(quotes))
        except Exception as e:
            print(f"Erreur lors de la récupération des données à l'offset {offset}: {e}")

        pbar.update(step)
        time.sleep(0.5)
        


## Scraping de ticker 
query='{\
  "operator": "AND",\
  "operands": [\
    {\
      "operator": "gt",\
      "operands": [\
        "avgdailyvol3m",\
        100000\
      ]\
    },\
    {\
      "operator": "btwn",\
      "operands": [\
        "lastclosemarketcap.lasttwelvemonths",\
        1000000000,\
        10000000000\
      ]\
    }\
  ]\
}'

response = json.loads(requests.post(url, verify=False, headers=get_headers(0), data=json.dumps(get_data(offset=0, query=query)), timeout=30).content)
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
    for offset in range(100, total_value, step):
        try:
            response = json.loads(requests.post(url, verify=False, headers=get_headers(offset), data=json.dumps(get_data(offset=offset, query=query)), timeout=30).content)
            quotes = response.get('finance', {}).get('result', [{}])[0].get('quotes', [])
            dfs.append(pd.DataFrame(quotes))
        except Exception as e:
            print(f"Erreur lors de la récupération des données à l'offset {offset}: {e}")

        pbar.update(step)
        time.sleep(0.5)



## Scraping de ticker 
query='{\
  "operator": "AND",\
  "operands": [\
    {\
      "operator": "gt",\
      "operands": [\
        "avgdailyvol3m",\
        100000\
      ]\
    },\
    {\
      "operator": "btwn",\
      "operands": [\
        "lastclosemarketcap.lasttwelvemonths",\
        1000000,\
        1000000000\
      ]\
    }\
  ]\
}'
response = json.loads(requests.post(url, verify=False, headers=get_headers(0), data=json.dumps(get_data(offset=0, query=query)), timeout=30).content)
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
    for offset in range(100, total_value, step):
        try:
            response = json.loads(requests.post(url, verify=False, headers=get_headers(offset), data=json.dumps(get_data(offset=offset, query=query)), timeout=30).content)
            quotes = response.get('finance', {}).get('result', [{}])[0].get('quotes', [])
            dfs.append(pd.DataFrame(quotes))
        except Exception as e:
            print(f"Erreur lors de la récupération des données à l'offset {offset}: {e}")

        pbar.update(step)
        time.sleep(0.5)



## Concaténer tous les DataFrames en un seul et dump dans un CSV
df_all_quotes = pd.concat(dfs, ignore_index=True)
# Supprimer les doublons basés sur une colonne spécifique
df_all_quotes = df_all_quotes.drop_duplicates(subset=['symbol'])
# Enregistrer le DataFrame dans un fichier CSV
df_all_quotes.to_csv('all_quotes_from_yahoo.csv', index=False)

