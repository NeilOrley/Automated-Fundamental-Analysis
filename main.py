
"""
Ce script Python est conçu pour extraire, analyser et évaluer des données financières d'entreprises à partir du site finviz.com. 
Il analyse ces données et les enregistre ensuite dans un fichier CSV pour une visualisation ultérieure. 
Voici une analyse détaillée de ce que fait chaque section du code :
    * Importations : Le script commence par importer un certain nombre de bibliothèques nécessaires à son fonctionnement.
    * Préparation initiale :
        ** Les warnings sont désactivés.
        ** La date du jour est définie.
        ** Des structures de données pour stocker les informations sont initialisées.
        ** Les métriques financières à analyser sont définies.
        ** L'URL de base pour le scraping est définie.
        ** Une liste d'agents utilisateurs (user agents) est chargée depuis un fichier pour simuler différentes requêtes de navigateur.
    * Fonctions de scraping et de traitement :
        ** getNumStocks(url): Récupère le nombre total d'actions à scraper sur le site.
        ** get_company_data(url, debug=False): Extrait les données du site web et les stocke dans des dataframes. Les données sont également sauvegardées dans un fichier CSV pour éviter de rescraping si nécessaire.
        ** remove_outliers(S, std): Supprime les valeurs aberrantes d'une série.
        ** get_sector_data(): Calcule des statistiques par secteur pour diverses métriques financières.
        ** get_metric_val(ticker, metric_name): Récupère la valeur d'une métrique pour une entreprise spécifique.
        ** convert_to_letter_grade(val): Convertit un score numérique en une note alphabétique.
        ** get_metric_grade(sector, metric_name, metric_val): Évalue une métrique pour une entreprise donnée par rapport à son secteur.
        ** get_category_grades(ticker, sector): Évalue une entreprise sur plusieurs catégories.
        ** get_dynamic_scale_factor(category_weights): Calcule un facteur d'échelle pour ajuster les scores.
        ** get_stock_rating(category_grades): Calcule une note globale pour une entreprise basée sur ses évaluations catégorielles.
        ** get_stock_rating_data(debug=False): Calcule et stocke les notes pour toutes les entreprises.
        ** export_to_csv(filename): Enregistre les données évaluées dans un fichier CSV.
    * Exécution : Le script exécute ensuite les fonctions dans l'ordre approprié pour scraper les données, les évaluer et les enregistrer dans un fichier CSV.

Points d'amélioration / Remarques :

La gestion des erreurs pourrait être améliorée. 
    Par exemple, lors de la récupération des données du site web, s'il y a un problème avec la requête, 
    le code pourrait essayer à nouveau après un certain temps ou sauter cette partie.
Utiliser un cache ou une base de données pour stocker les données plutôt qu'un fichier CSV pourrait améliorer la performance et la flexibilité.
Le script pourrait bénéficier d'une meilleure modularisation, en déplaçant le code d'initialisation et les constantes dans des fichiers ou des classes séparés.
Pour éviter de se faire bannir par le site lors du scraping, il serait judicieux d'ajouter des délais plus longs ou d'utiliser des proxies.

Note : le scraping de sites web sans permission peut enfreindre les conditions d'utilisation du site et / ou la loi dans certaines juridictions.
"""

"""
Idées :
    Compare companies within the same sector for valuation.
    Look at dividend-paying companies and their payout ratios.
    Analyze companies based on growth metrics like "EPS next 5Y" or "Sales past 5Y".
    Understand the liquidity of a company based on 'Curr R' and 'Quick R'.
    Look for stocks that are potentially overbought or oversold based on the RSI.
"""



from datetime import date 
from scraper import URL, get_company_data
from rate import get_sector_data, get_stock_rating_data, export_to_csv
from filter import get_stocks_with_best_potential



# Définition de la date du jour au format souhaité
today_date = date.today().strftime("%m/%d/%y").replace('/', '.')


# Lancement du scraping et des calculs       
allStockData = get_company_data(URL, debug=True)
get_sector_data(allStockData)
get_stock_rating_data(allStockData)
export_to_csv(allStockData, f"StockRatings-{today_date}.csv")

companies_with_best_potential = get_stocks_with_best_potential(allStockData, percentile_rate=0.95, min_quick_r=1.0, min_curr_r=1.5, max_rsi=30)
