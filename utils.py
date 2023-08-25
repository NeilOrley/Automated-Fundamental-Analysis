import pandas as pd
import numpy as np
from tqdm import tqdm      
from constants import allStockData, grading_metrics, grade_scores
from datetime import date 
import collections

# Définition de la date du jour au format souhaité
today_date = date.today().strftime("%m/%d/%y").replace('/', '.')

sector_data = collections.defaultdict(lambda : collections.defaultdict(dict))
data_to_add = collections.defaultdict(list)

def remove_outliers(S, std):    
    s1 = S[~((S-S.mean()).abs() > std * S.std())]
    return s1[~((s1-s1.mean()).abs() > std * s1.std())]


"""
Cette fonction prend les données de stocks (allStockData), extrait les secteurs uniques et certaines métriques. 
Ensuite, elle parcourt chaque secteur et, pour chaque secteur, parcourt chaque métrique. 
Les étapes effectuées sont les suivantes :
    Les lignes correspondant au secteur actuel sont extraites du DataFrame allStockData.
    Les valeurs de pourcentage dans la colonne de métrique sont nettoyées et converties en valeurs numériques à l'aide de str.rstrip('%') et pd.to_numeric(). 
        Les valeurs manquantes sont gérées en utilisant errors='coerce'.
    Les valeurs aberrantes (outliers) sont supprimées en appelant la fonction remove_outliers().
    Différentes statistiques (médiane, quantiles, écart-type) sont calculées pour la métrique actuelle et le secteur actuel 
    et stockées dans le dictionnaire sector_data en utilisant les clés correspondantes.
"""
# Fonction pour calculer les statistiques par secteur pour différentes métriques
def get_sector_data(allStockData):
    
    # Obtention de la liste des secteurs uniques dans les données
    sectors = allStockData['Sector'].unique()
    
    # Obtention de la liste des métriques (colonnes) à partir de l'index 7 jusqu'à l'avant-dernier
    metrics = allStockData.columns[7: -3]

    # Parcours de chaque secteur
    for sector in sectors:
        
        # Extraction des lignes correspondant au secteur actuel
        rows = allStockData.loc[allStockData['Sector'] == sector]
        
        # Parcours de chaque métrique
        for metric in metrics:
            
            # Nettoyage des valeurs de pourcentage, les convertissant en valeurs numériques (avec des valeurs manquantes gérées)
            rows[metric] = rows[metric].str.rstrip('%')
            rows[metric] = pd.to_numeric(rows[metric], errors='coerce')
            
            # Suppression des valeurs aberrantes (outliers) en utilisant la fonction remove_outliers (non définie dans le code)
            data = remove_outliers(rows[metric], 2)
            
            # Calcul des statistiques pour la métrique actuelle et le secteur actuel
            sector_data[sector][metric]['Median'] = data.median(skipna=True)
            sector_data[sector][metric]['5Pct'] = data.quantile(0.05)
            sector_data[sector][metric]['10Pct'] = data.quantile(0.1)
            sector_data[sector][metric]['90Pct'] = data.quantile(0.9)
            sector_data[sector][metric]['95Pct'] = data.quantile(0.95)
            # Pourquoi l'écart type est-il divisé par 5 ?
            #sector_data[sector][metric]['Std'] = np.std(data, axis=0) / 5    
            sector_data[sector][metric]['Std'] = np.std(data, axis=0)


# Récupération de la valeur d'une métrique pour un ticker donné
def get_metric_val(allStockData, ticker, metric_name):
    try:
        return float(str(allStockData.loc[allStockData['Ticker'] == ticker][metric_name].values[0]).rstrip("%"))
    except:
        try:
            # Si les données ne sont pas dispobibles essaye d'affecter la valeur médiane du secteur calculée par get_sector_data()
            sector = str(allStockData.loc[allStockData['Ticker'] == ticker]['Sector'].values[0])
            return float(sector_data[sector][metric_name]['Median'])
        except:
            return 0


"""
Cette fonction prend une valeur val et la compare aux scores associés à chaque note dans le dictionnaire grade_scores. 
Les scores et les notes sont classés dans l'ordre décroissant. 
La fonction parcourt ce dictionnaire dans cet ordre et dès que la valeur val est supérieure ou égale au score associé à une note, 
la fonction retourne cette note sous forme de lettre.
Par exemple, si val est égal à 3.2, la fonction parcourra les notes du dictionnaire et retournera 'B', car 3.2 est supérieur ou égal au score de 'B' (3.0).
"""
# Fonction pour convertir une valeur en note sous forme de lettre
def convert_to_letter_grade(val):
        
    # Parcours des notes dans l'ordre décroissant
    for grade in grade_scores:
        # Si la valeur est supérieure ou égale au score associé à la note
        if val >= grade_scores[grade]:
            # Retourne la note sous forme de lettre
            return grade




"""
Cette fonction, get_metric_grade, prend en entrée un secteur, 
le nom d'une métrique et une valeur de métrique, 
et renvoie une note correspondante à cette valeur de métrique.

Améliorations possibles :
    Utiliser des seuils personnalisés : 
        Au lieu d'utiliser uniquement les 10e et 90e percentiles du secteur, 
        définir des seuils personnalisés en fonction d'un contexte spécifique. 
        Par exemple, définir des seuils basés sur des benchmarks de l'industrie ou des normes spécifiques à un domaine d'activité.

    Prendre en compte la signification de chaque métrique : 
        Certaines métriques peuvent avoir une importance plus élevée que d'autres pour évaluer la performance 
        d'une entreprise dans un secteur donné. Attribuer des poids différents aux métriques en fonction 
        de leur pertinence pour obtenir une note globale plus précise.

        Fwd P/E (Price-to-Earnings ratio futur) : 
            Ce ratio est souvent utilisé pour évaluer la valorisation d'une entreprise. 
            Un poids élevé peut être attribué à cette métrique, car elle fournit une indication 
            importante de la perception du marché concernant les perspectives de croissance future de l'entreprise.
        PEG (Price/Earnings to Growth ratio) : 
            Le PEG ratio est une mesure de la valorisation d'une entreprise ajustée en fonction de sa croissance future attendue. 
            Il peut être utilisé pour évaluer si une entreprise est sous-évaluée ou surévaluée par rapport à sa croissance prévue. 
            Une importance similaire au Fwd P/E peut être accordée à cette métrique.
        P/S (Price-to-Sales ratio) : 
            Le P/S ratio est utilisé pour évaluer la valorisation d'une entreprise par rapport à ses revenus. 
            Le poids attribué à cette métrique peut dépendre du secteur spécifique, car certains secteurs ont 
            tendance à avoir des marges bénéficiaires plus élevées que d'autres.
        P/B (Price-to-Book ratio) : 
            Le P/B ratio est utilisé pour évaluer la valorisation d'une entreprise par rapport à la valeur 
            comptable de ses actifs. Le poids attribué à cette métrique peut varier en fonction du secteur, 
            car certains secteurs ont une dépendance plus forte aux actifs tangibles que d'autres.
        P/FCF (Price-to-Free Cash Flow ratio) : 
            Le P/FCF ratio est utilisé pour évaluer la valorisation d'une entreprise par rapport à son flux de trésorerie disponible. 
            Cette métrique peut être particulièrement pertinente pour évaluer la capacité d'une entreprise à générer des liquidités. 
            Le poids attribué dépendra du secteur et de l'importance du flux de trésorerie dans l'analyse financière du secteur.
        Volatility M (Volatilité) : 
            La volatilité est une mesure du degré de variation des prix d'une entreprise. 
            Le poids attribué à cette métrique peut dépendre du niveau de risque acceptable dans le secteur spécifique. 
            Certains secteurs plus volatils, tels que les secteurs technologiques, peuvent accorder une plus grande importance à cette métrique.

    Considérer la relation entre les métriques : 
        Parfois, plusieurs métriques sont interdépendantes et leur combinaison peut fournir une meilleure évaluation globale. 
        Ajouter des règles spécifiques pour prendre en compte ces relations et ajuster la note en conséquence. (P/E & FwdP/E)

"""
def get_metric_grade(sector, metric_name, metric_val):
    
    # Vérifie si le nom de la métrique se trouve dans la liste des métriques spécifiques. 
    # Si c'est le cas, la variable lessThan est définie comme True, sinon elle est définie comme False. 
    # Cela est utilisé ultérieurement pour déterminer si la comparaison de la métrique doit être inférieure ou supérieure à une valeur de référence.
    lessThan = metric_name in ['Fwd P/E', 'PEG', 'P/S', 'P/B', 'P/FCF', 'Volatility M']    

    # Définit la base de notation en fonction de la valeur de lessThan. 
    # Si lessThan est True, la base de notation est définie sur '10Pct', sinon elle est définie sur '90Pct'.
    grade_basis = '10Pct' if lessThan else '90Pct'
    
    # Récupère les valeurs de départ et de changement à partir de la variable sector_data. 
    start, change = sector_data[sector][metric_name][grade_basis], sector_data[sector][metric_name]['Std']
    
    # Définit une correspondance entre les notes et les valeurs de changement. 
    # Les notes sont utilisées comme clés et les valeurs de changement sont utilisées comme valeurs correspondantes.
    grade_map = {'A+': 0, 'A': change, 'A-' : change * 2, 'B+' : change * 3, 'B' : change * 4, 
                 'B-' : change * 5, 'C+' : change * 6, 'C' : change * 7, 'C-' : change * 8, 
                 'D+' : change * 9, 'D' : change * 10, 'D-' : change * 11, 'F' : change * 12}
    
    
    for grade, val in grade_map.items():
        
        # Calcule la valeur de comparaison en ajoutant ou soustrayant la valeur de changement (val) à la valeur de départ (start), en fonction de la valeur de lessThan. 
        # Si lessThan est True, la valeur de comparaison est augmentée, sinon elle est diminuée.
        comparison = start + val if lessThan else start - val

        # Vérifie si lessThan est True et si la valeur de la métrique (metric_val) est inférieure à la valeur de comparaison. 
        # Si les deux conditions sont satisfaites, la fonction renvoie la note correspondante (grade).
        if lessThan and metric_val < comparison:            
            return grade
        
        # Vérifie si lessThan est False (équivalent à not lessThan) et si la valeur de la métrique (metric_val) est supérieure à la valeur de comparaison. 
        # Si les deux conditions sont satisfaites, la fonction renvoie la note correspondante (grade).
        if lessThan == False and metric_val > comparison:            
            return grade
    # Si aucune des conditions précédentes n'est satisfaite, la fonction renvoie la note par défaut 'C'.        
    return 'C'


"""
Cette fonction calcule les notes par catégorie pour un ticker d'entreprise donné en utilisant certaines métriques de notation. 
Elle parcourt les catégories et les métriques associées, obtient les notes de chaque métrique, 
puis calcule et stocke les notes moyennes pour chaque catégorie.
"""
# Fonction pour calculer les notes par catégorie pour un ticker donné dans un secteur donné
def get_category_grades(allStockData, ticker, sector):
    
    # Dictionnaire qui stockera les notes par catégorie
    category_grades = {}
    
    # Parcours de chaque catégorie définie dans grading_metrics
    for category in grading_metrics:
        
        # Liste pour stocker les notes de chaque métrique dans la catégorie actuelle
        metric_grades = []
        # Parcours de chaque métrique dans la catégorie
        if ticker == '':
            for metric_name in grading_metrics[category]:
                #print(f"ticker={ticker}, metric_name={metric_name}")
                # Le ticker étant vide, la note moyenne est affectée : Ne devrait pas arriver
                metric_grades.append('C')
        else:
            for metric_name in grading_metrics[category]:
                #print(f"ticker={ticker}, metric_name={metric_name}")
                # Appel à la fonction get_metric_grade pour obtenir la note de la métrique actuelle
                metric_grades.append(get_metric_grade(sector, metric_name, get_metric_val(allStockData, ticker, metric_name)))
            
        # Stockage des notes de chaque métrique dans la catégorie actuelle
        category_grades[category] = metric_grades
        
    # Calcul de la note moyenne pour chaque catégorie
    for category in category_grades:
        
        score = 0
        
        # Calcul de la somme des scores associés à chaque note dans la catégorie
        for grade in category_grades[category]:
            score += grade_scores[grade]
        
        # Calcul de la note moyenne en divisant la somme des scores par le nombre de notes dans la catégorie
        category_grades[category].append(round(score / len(category_grades[category]), 2))
        
    # Retourne le dictionnaire contenant les notes par catégorie avec les moyennes
    return category_grades


"""
Calcule le score ajusté d'un stock basé sur les notes par catégorie.

Args:
- category_grades (dict): Un dictionnaire où la clé est la catégorie 
    et la valeur est une liste de notes pour cette catégorie.

Returns:
- float: Le score ajusté arrondi à deux décimales.
"""
def get_stock_rating(category_grades):
    # Initialisation du score total à 0
    score = 0
    
    # Pour chaque catégorie dans le dictionnaire category_grades
    for category in category_grades:
        # Trouver la valeur maximale dans le dictionnaire grade_scores
        max_value = max(grade_scores.values())
        
        # Prendre le dernier élément de la liste associée à la catégorie courante
        # Diviser par la valeur maximale et multiplier par 100 pour obtenir une valeur normalisée
        normalized_value = (category_grades[category][-1] / max_value) * 100
        
        # Ajouter la valeur normalisée au score total
        score += normalized_value
        

    # Calculer le nombre total de catégories
    number_of_categories = len(category_grades)
    
    # Retourner la moyenne des scores normalisés, arrondie à deux décimales
    return round(score/number_of_categories, 2)

    
"""
Cette fonction prend les données de stocks (allStockData), 
calcule les notes par catégorie et les notes globales pour chaque ticker, 
puis ajoute ces données calculées aux listes appropriées dans le dictionnaire data_to_add. 
La fonction utilise une barre de progression (tqdm) pour suivre le progrès du calcul 
et offre également une option de débogage pour arrêter le traitement 
après un certain nombre de tickers (10).
"""
# Fonction pour calculer les notes et les évaluations pour tous les tickers
def get_stock_rating_data(allStockData,debug=False):
        
    # Compteur pour suivre le progrès
    counter = 0
    print('\nCalculating Stock Ratings...\n')

    # Utilisation de tqdm pour afficher une barre de progression
    with tqdm(total = allStockData.shape[0]) as pbar:
        
        # Parcours de chaque ligne dans le DataFrame allStockData
        for row in allStockData.iterrows():
            
            # Extraction du ticker et du secteur de la ligne actuelle
            ticker, sector = row[1]['Ticker'], row[1]['Sector']
            
            if ticker != '' :            
                # Obtention des notes par catégorie pour le ticker et le secteur actuels
                category_grades = get_category_grades(allStockData, ticker, sector)
                
                # Calcul de la note globale du stock en utilisant les notes par catégorie
                stock_rating = get_stock_rating(category_grades)
                
                # Ajout des données calculées aux listes correspondantes dans data_to_add
                data_to_add['Overall Rating'].append(stock_rating)
                data_to_add['Valuation Grade'].append(convert_to_letter_grade(category_grades['Valuation'][-1]))
                data_to_add['Profitability Grade'].append(convert_to_letter_grade(category_grades['Profitability'][-1]))
                data_to_add['Growth Grade'].append(convert_to_letter_grade(category_grades['Growth'][-1]))
                data_to_add['Performance Grade'].append(convert_to_letter_grade(category_grades['Performance'][-1]))
                
                # Décommentez les lignes suivantes pour afficher des informations de débogage
                # print(row[1]['Ticker'])
                # print(category_grades)
                # print(stock_rating)
                # print()   
                
                # Mise à jour du compteur et de la barre de progression
                counter += 1 
                pbar.update(1)
                
                # Condition pour le mode de débogage
                if debug == True and counter == 10:
                    break

    
# Export des résultats dans un CSV    
def export_to_csv(allStockData, filename):
        
    allStockData['Overall Rating'] = data_to_add['Overall Rating']
    allStockData['Valuation Grade'] = data_to_add['Valuation Grade']
    allStockData['Profitability Grade'] = data_to_add['Profitability Grade']
    allStockData['Growth Grade'] = data_to_add['Growth Grade']
    allStockData['Performance Grade'] = data_to_add['Performance Grade']    
    allStockData['Percent Diff'] = (pd.to_numeric(allStockData['Target Price'], errors='coerce') - pd.to_numeric(allStockData['Price'], errors='coerce')) / pd.to_numeric(allStockData['Price'], errors='coerce') * 100

    ordered_columns = 'Ticker, Company, Market Cap, Overall Rating, Sector, Industry, Country, Valuation Grade, Profitability Grade, Growth Grade, Performance Grade, Fwd P/E, PEG, P/S, P/B, P/C, P/FCF, Dividend, Payout Ratio, EPS this Y, EPS next Y, EPS past 5Y, EPS next 5Y, Sales past 5Y, EPS Q/Q, Sales Q/Q, Insider Own, Insider Trans, Inst Own, Inst Trans, Short Ratio, ROA, ROE, ROI, Curr R, Quick R, LTDebt/Eq, Debt/Eq, Gross M, Oper M, Profit M, Perf Month, Perf Quart, Perf Half, Perf Year, Perf YTD, Volatility M, SMA20, SMA50, SMA200, 52W High, 52W Low, RSI, Earnings, Price, Target Price, Percent Diff'

    stock_csv_data = allStockData
    stock_csv_data = allStockData[ordered_columns.replace(', ', ',').split(',')]
    stock_csv_data.to_csv(filename, index=False)
    
    print('\nSaved as', f"StockRatings-{today_date}.csv")
    
      