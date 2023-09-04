import pandas as pd
import numpy as np

# Simuler des données : rendements de l'actif et rendements du marché
# Dans la réalité, vous les obtiendriez probablement à partir d'une source de données financières
asset_returns = pd.Series([0.03, 0.04, -0.02, -0.01, 0.02])
market_returns = pd.Series([0.02, 0.03, -0.01, -0.02, 0.01])

# Calculer le bêta
covariance = np.cov(asset_returns, market_returns)[0][1]
variance = np.var(market_returns)
beta = covariance / variance

print("Coefficient bêta :", beta)
