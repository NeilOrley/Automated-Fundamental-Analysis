import pandas as pd





# Fonction pour convertir la colonne 'Market Cap' en milliards
def convert_market_cap(value):
    try:
        if 'B' in value:
            return float(value[:-1])
        elif 'M' in value:
            return float(value[:-1]) / 1000
        else:
            return float(value)
    except (ValueError, TypeError):
        return None  # ou 0 ou toute autre valeur par défaut


"""
Cette fonction filtre les société ayant un market cap supérieur à 1 milliard
puis réalise un 95 eme percentile sur la note globale calculée
conserve les actions répondant a ces critères dans un CSV et retourne le dataframe filtré.
"""
def get_stocks_with_best_potential(allStockData, percentile_rate=0.95, min_quick_r=1.0, min_curr_r=1.5, max_rsi=30):
    
    # Convertir les colonnes pertinentes en numéros à virgule flottante
    allStockData['Market Cap'] = allStockData['Market Cap'].apply(convert_market_cap)
    allStockData['Quick R'] = pd.to_numeric(allStockData['Quick R'], errors='coerce')
    allStockData['Curr R'] = pd.to_numeric(allStockData['Curr R'], errors='coerce')
    allStockData['RSI'] = pd.to_numeric(allStockData['RSI'], errors='coerce')

    # Supprimer les lignes où les colonnes pertinentes sont None ou NaN
    allStockData.dropna(subset=['Market Cap', 'Quick R', 'Curr R', 'RSI'], inplace=True)

    # Appliquer des filtres supplémentaires pour Quick R, Curr R et RSI
    allStockData = allStockData[(allStockData['Quick R'] >= min_quick_r) & 
                                (allStockData['Curr R'] >= min_curr_r) & 
                                (allStockData['RSI'] <= max_rsi)]

    # Grouper les données par secteur et calculer le percentile spécifié de "Overall Rating" pour chaque groupe
    percentile_by_sector = allStockData.groupby('Sector')['Overall Rating'].quantile(percentile_rate)

    # DataFrame vide pour stocker les résultats
    result_df = pd.DataFrame()

    # Parcourir chaque secteur et trouver les tickers avec "Overall Rating" supérieur au percentile spécifié
    for sector, percentile_value in percentile_by_sector.items():
        filtered_df = allStockData[(allStockData['Sector'] == sector) & (allStockData['Overall Rating'] > percentile_value)]
        result_df = pd.concat([result_df, filtered_df])

    # Enregistrez les résultats dans un fichier CSV
    result_df.to_csv(f'companies_with_best_potential_over_{int(percentile_rate*100)}p.csv', index=False)

    return result_df


