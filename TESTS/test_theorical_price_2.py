def calculate_dcf(free_cash_flows, discount_rate, terminal_growth_rate, num_shares):
    """
    Calcule la valeur théorique de l'action en utilisant la méthode des Flux de Trésorerie Actualisés (DCF).

    Args:
    free_cash_flows (list of float) : Une liste des flux de trésorerie libres prévus pour chaque année future.
    discount_rate (float) : Le taux d'actualisation à utiliser, en pourcentage.
    terminal_growth_rate (float) : Le taux de croissance perpétuel des flux de trésorerie, en pourcentage.
    num_shares (int) : Le nombre total d'actions en circulation.

    Returns:
    float : La valeur théorique de l'action.
    """

    discounted_cash_flows = []
    for i, cash_flow in enumerate(free_cash_flows):
        discounted_cash_flow = cash_flow / ((1 + discount_rate / 100) ** (i + 1))
        discounted_cash_flows.append(discounted_cash_flow)

    # Calcul de la valeur terminale
    last_projected_year_cash_flow = free_cash_flows[-1]
    terminal_value = last_projected_year_cash_flow * (1 + terminal_growth_rate / 100) / (discount_rate / 100 - terminal_growth_rate / 100)
    discounted_terminal_value = terminal_value / ((1 + discount_rate / 100) ** len(free_cash_flows))

    # Calcul de la valeur totale de l'entreprise
    enterprise_value = sum(discounted_cash_flows) + discounted_terminal_value

    # Calcul de la valeur par action
    stock_value = enterprise_value / num_shares

    return stock_value

# Exemple d'utilisation
# Supposons des flux de trésorerie libres de 50M$, 55M$, 60M$ pour les 3 prochaines années
free_cash_flows = [103412000000, 111004000000, 118862000000]

# Supposons un taux d'actualisation de 10%
discount_rate = 8.80

# Supposons un taux de croissance terminal de 3%
terminal_growth_rate = 3.6

# Supposons 10 millions d'actions en circulation
num_shares = 15851775392

# Calculer la valeur théorique de l'action
theoretical_stock_value = calculate_dcf(free_cash_flows, discount_rate, terminal_growth_rate, num_shares)

print(f"La valeur théorique de l'action est de {theoretical_stock_value:.2f}$")