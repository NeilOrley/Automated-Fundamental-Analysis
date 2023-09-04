def evaluate_stock_by_pe_ratio(target_pe_ratio, company_earnings_per_share):
    """
    Calcule la valeur théorique de l'action en utilisant le ratio P/E cible et les bénéfices par action de l'entreprise.
    
    Args:
    target_pe_ratio (float) : Le ratio P/E cible, généralement la moyenne du secteur ou de l'industrie.
    company_earnings_per_share (float) : Les bénéfices par action de l'entreprise.
    
    Returns:
    float : La valeur théorique de l'action.
    """
    return target_pe_ratio * company_earnings_per_share

# Exemple d'utilisation
# Supposons que le ratio P/E moyen du secteur soit de 20
target_pe_ratio = 27.70

# Supposons que les bénéfices par action de l'entreprise soient de 5$
company_earnings_per_share = 5.97

# Calculer la valeur théorique de l'action
theoretical_stock_value = evaluate_stock_by_pe_ratio(target_pe_ratio, company_earnings_per_share)

print(f"La valeur théorique de l'action est de {theoretical_stock_value}$")
