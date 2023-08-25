
# Dictionnaires pour stocker les données récupérées
allStockData = {}
tickers = []
dataframes = []

# Dictionnaire contenant les scores associés à chaque grade
grade_scores = {'A+' : 4.3, 'A' : 4.0, 'A-' : 3.7, 'B+' : 3.3, 'B' : 3.0, 'B-' : 2.7, 
                'C+' : 2.3, 'C' : 2.0, 'C-' : 1.7, 'D+' : 1.3, 'D' : 1.0, 'D-' : 0.7, 'F' : 0.0}

# Définition des métriques financières à analyser par catégorie
grading_metrics = {
    'Valuation' : ['Fwd P/E', 'PEG', 'P/S', 'P/B', 'P/FCF'],
    'Profitability' : ['Profit M', 'Oper M', 'Gross M', 'ROE', 'ROA'],
    'Growth' : ['EPS this Y', 'EPS next Y', 'EPS next 5Y', 'Sales Q/Q', 'EPS Q/Q'],
    'Performance' : ['Perf Month', 'Perf Quart', 'Perf Half', 'Perf Year', 'Perf YTD', 'Volatility M']
}

# URL de la page d'où récupérer les données
URL = 'https://finviz.com/screener.ashx?v=152&c=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,21,22,23,26,27,28,29,31,32,33,34,35,36,37,38,39,40,41,43,44,45,46,47,51,52,53,54,57,58,59,65,68,69'


"""
Ce code lit un fichier nommé "useragents.txt", où chaque ligne contient un user-agent. 
Il enlève les sauts de ligne de chaque user-agent et les stocke dans une liste appelée userAgentList.
"""
# Création d'une liste vide pour stocker les user-agents
userAgentList = []
# Ouverture du fichier 'useragents.txt' en mode lecture ('r' pour 'read')
useragents = open("useragents.txt", "r")
# Parcours de chaque ligne du fichier
for line in useragents:
    # Suppression du caractère de nouvelle ligne ('\n') et ajout de la ligne modifiée à la liste
    userAgentList.append(line.replace('\n', ''))    
# Fermeture du fichier après avoir terminé de lire son contenu
useragents.close()