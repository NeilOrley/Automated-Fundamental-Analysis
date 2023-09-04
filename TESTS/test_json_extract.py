import pandas as pd
import json

def load_json(json_str):
    return json.loads(json_str)

def extract_data_from_json(data_dict):
    return data_dict['quoteSummary']['result'][0]

def convert_to_dataframe(data):
    raw_data = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    raw_value = sub_value.get("raw", "N/A")
                    raw_data[f"{key}_{sub_key}"] = raw_value
                    
    return pd.Series(raw_data)

def update_existing_dataframe(existing_df, new_data_series, symbol):
    # Trouver l'index de la ligne pour le symbole spécifié
    index_to_update = existing_df[existing_df['symbol'] == symbol].index[0]
    
    # Mettre à jour les données pour le symbole spécifié
    for col in new_data_series.index:
        if col not in existing_df.columns:
            existing_df[col] = None
        existing_df.loc[index_to_update, col] = new_data_series[col]

if __name__ == '__main__':
    # Le JSON donné en tant que string
    json_str = '{"quoteSummary":{"result":[{"defaultKeyStatistics":{"maxAge":1,"priceHint":{"raw":2,"fmt":"2","longFmt":"2"},"enterpriseValue":{"raw":605706688397312,"fmt":"605.71T","longFmt":"605,706,688,397,312"},"forwardPE":{},"profitMargins":{"raw":0.07717,"fmt":"7.72%"},"floatShares":{"raw":16159604853,"fmt":"16.16B","longFmt":"16,159,604,853"},"sharesOutstanding":{"raw":67659001856,"fmt":"67.66B","longFmt":"67,659,001,856"},"sharesShort":{},"sharesShortPriorMonth":{},"sharesShortPreviousMonthDate":{},"dateShortInterest":{},"sharesPercentSharesOut":{},"heldPercentInsiders":{"raw":0.0,"fmt":"0.00%"},"heldPercentInstitutions":{"raw":0.0,"fmt":"0.00%"},"shortRatio":{},"shortPercentOfFloat":{},"beta":{"raw":0.574564,"fmt":"0.57"},"impliedSharesOutstanding":{"raw":67659001856,"fmt":"67.66B","longFmt":"67,659,001,856"},"morningStarOverallRating":{},"morningStarRiskRating":{},"category":null,"bookValue":{"raw":1399.1775,"fmt":"1,399.18"},"priceToBook":{"raw":19.219864,"fmt":"19.22"},"annualReportExpenseRatio":{},"ytdReturn":{},"beta3Year":{},"totalAssets":{},"yield":{},"fundFamily":null,"fundInceptionDate":{},"legalType":null,"threeYearAverageReturn":{},"fiveYearAverageReturn":{},"priceToSalesTrailing12Months":{},"lastFiscalYearEnd":{"raw":1680220800,"fmt":"2023-03-31"},"nextFiscalYearEnd":{"raw":1711843200,"fmt":"2024-03-31"},"mostRecentQuarter":{"raw":1688083200,"fmt":"2023-06-30"},"earningsQuarterlyGrowth":{"raw":0.78,"fmt":"78.00%"},"revenueQuarterlyGrowth":{},"netIncomeToCommon":{"raw":3025869996032,"fmt":"3.03T","longFmt":"3,025,869,996,032"},"trailingEps":{"raw":107.57,"fmt":"107.57"},"forwardEps":{},"pegRatio":{},"lastSplitFactor":null,"lastSplitDate":{},"enterpriseToRevenue":{"raw":15.448,"fmt":"15.45"},"enterpriseToEbitda":{"raw":122.416,"fmt":"122.42"},"52WeekChange":{"raw":2.154672,"fmt":"215.47%"},"SandP52WeekChange":{"raw":0.14866495,"fmt":"14.87%"},"lastDividendValue":{"raw":0.352414,"fmt":"0.35"},"lastDividendDate":{"raw":1664409600,"fmt":"2022-09-29"},"lastCapGain":{},"annualHoldingsTurnover":{}},"calendarEvents":{"maxAge":1,"earnings":{"earningsDate":[],"earningsAverage":{},"earningsLow":{},"earningsHigh":{},"revenueAverage":{},"revenueLow":{},"revenueHigh":{}},"exDividendDate":{"raw":1680134400,"fmt":"2023-03-30"},"dividendDate":{}},"financialData":{"maxAge":86400,"currentPrice":{"raw":26892.0,"fmt":"26,892.00"},"targetHighPrice":{},"targetLowPrice":{},"targetMeanPrice":{},"targetMedianPrice":{},"recommendationMean":{},"recommendationKey":"none","numberOfAnalystOpinions":{},"totalCash":{"raw":10193719001088,"fmt":"10.19T","longFmt":"10,193,719,001,088"},"totalCashPerShare":{"raw":470.254,"fmt":"470.25"},"ebitda":{"raw":4947951222784,"fmt":"4.95T","longFmt":"4,947,951,222,784"},"totalDebt":{"raw":32016294739968,"fmt":"32.02T","longFmt":"32,016,294,739,968"},"quickRatio":{"raw":0.891,"fmt":"0.89"},"currentRatio":{"raw":1.109,"fmt":"1.11"},"totalRevenue":{"raw":39210014736384,"fmt":"39.21T","longFmt":"39,210,014,736,384"},"debtToEquity":{"raw":102.372,"fmt":"102.37%"},"revenuePerShare":{"raw":1800.0569,"fmt":"1,800.06"},"returnOnAssets":{"raw":0.02686,"fmt":"2.69%"},"returnOnEquity":{"raw":0.10277,"fmt":"10.28%"},"grossProfits":{},"freeCashflow":{"raw":-1262256128000,"fmt":"-1.26T","longFmt":"-1,262,256,128,000"},"operatingCashflow":{"raw":3549206937600,"fmt":"3.55T","longFmt":"3,549,206,937,600"},"earningsGrowth":{"raw":0.803,"fmt":"80.30%"},"revenueGrowth":{"raw":0.242,"fmt":"24.20%"},"grossMargins":{"raw":0.17813998,"fmt":"17.81%"},"ebitdaMargins":{"raw":0.12619,"fmt":"12.62%"},"operatingMargins":{"raw":0.083330005,"fmt":"8.33%"},"profitMargins":{"raw":0.07717,"fmt":"7.72%"},"financialCurrency":"JPY"}}],"error":null}}'
    
    # Charger le JSON dans un dictionnaire Python
    data_dict = load_json(json_str)
    
    # Extraire les données spécifiques
    result_data = extract_data_from_json(data_dict)
    
    # Convertir les données en DataFrame
    new_data_series = convert_to_dataframe(result_data)
    
    # Existant DataFrame
    existing_df_data = {
        'symbol': ['BBCA.JK', 'BBRI.JK', 'GOOGL.BA', 'BMRI.JK'],
        'twoHundredDayAverageChangePercent': [0.046306115, 0.10775926, 1.0906088, 0.14337595],
        'averageAnalystRating': ['2.6 - Hold', '1.7 - Buy', '', '1.8 - Buy'],
        'fiftyTwoWeekLowChangePercent': [0.15625, 0.3207547, 3.034091, 0.40828404],
        'language': ['en-US', 'en-US', 'en-US', 'en-US'],
        'dividendYield': [3.7, 5.19, None, 4.41]
    }
    existing_df = pd.DataFrame(existing_df_data)
    
    # Mettre à jour le DataFrame existant
    update_existing_dataframe(existing_df, new_data_series, 'GOOGL.BA')
    
    # Écrire le DataFrame actualisé dans un fichier CSV
    existing_df.to_csv("updated_data.csv", index=False)
    
    # Afficher le DataFrame actualisé
    print(existing_df)