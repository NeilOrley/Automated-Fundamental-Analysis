# Calcul du Coût des Capitaux Propres en utilisant le CAPM
def calculate_cost_of_equity(risk_free_rate, beta, market_return):
    return risk_free_rate + beta * (market_return - risk_free_rate)

# Calcul du Coût de la Dette après impôts
def calculate_after_tax_cost_of_debt(interest_rate, tax_rate):
    return interest_rate * (1 - tax_rate)

# Calcul du WACC
def calculate_wacc(cost_of_equity, cost_of_debt, equity_value, debt_value, tax_rate):
    total_value = equity_value + debt_value
    equity_weight = equity_value / total_value
    debt_weight = debt_value / total_value
    wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
    return wacc

# Exemple d'utilisation
# Taux sans risque, souvent basé sur les obligations d'État à long terme (en pourcentage)
risk_free_rate = 1.0

# Coefficient bêta de l'actif
beta = 1.2

# Rendement attendu du marché (en pourcentage)
market_return = 7.0

# Taux d'intérêt de la dette (en pourcentage)
interest_rate = 4.0

# Taux d'imposition sur les sociétés (en pourcentage)
tax_rate = 0.3

# Valeur des capitaux propres (en dollars)
equity_value = 1_000_000

# Valeur de la dette (en dollars)
debt_value = 500_000

# Calcul du coût des capitaux propres en utilisant le CAPM
cost_of_equity = calculate_cost_of_equity(risk_free_rate, beta, market_return)
print(f"Coût des capitaux propres (CAPM): {cost_of_equity:.2f}%")

# Calcul du coût de la dette après impôts
cost_of_debt = calculate_after_tax_cost_of_debt(interest_rate, tax_rate)
print(f"Coût de la dette après impôts: {cost_of_debt:.2f}%")

# Calcul du WACC
wacc = calculate_wacc(cost_of_equity, cost_of_debt, equity_value, debt_value, tax_rate)
print(f"Coût Moyen Pondéré du Capital (WACC): {wacc:.2f}%")
