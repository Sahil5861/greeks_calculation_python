import math
from scipy.stats import norm

def calculate_greeks(option_type, S, K, T, sigma, r):
    """
    Calculates Delta, Gamma, Theta, and Vega for a given option contract.

    Args:
    option_type (str): 'Call' or 'Put'
    S (float): Underlying asset price
    K (float): Strike price
    T (float): Time to expiration in years
    sigma (float): Volatility (as a decimal)
    r (float): Risk-free interest rate (as a decimal)

    Returns:
    dict: A dictionary containing Delta, Gamma, Theta, and Vega
    """
    # Input validation
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0 or r < 0:
        raise ValueError("All input values must be positive.")
    
    # Black-Scholes formula for calculating option price
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type.lower() == 'call':
        # Delta calculation for Call option
        delta = math.exp(-r * T) * norm.cdf(d1)
    elif option_type.lower() == 'put':
        # Delta calculation for Put option
        delta = -math.exp(-r * T) * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Please choose 'Call' or 'Put'.")

    # Gamma calculation
    gamma = math.exp(-r * T) * norm.pdf(d1) / (S * sigma * math.sqrt(T))

    # Theta calculation
    theta = -(S * norm.pdf(d1) * sigma * math.exp(-r * T)) / (2 * math.sqrt(T)) \
            - r * K * math.exp(-r * T) * norm.cdf(d2)
    if option_type.lower() == 'call':
        theta += r * S * norm.cdf(d1)
    else:
        theta += r * S * norm.cdf(-d1)

    # Vega calculation
    vega = S * math.sqrt(T) * norm.pdf(d1)

    return {'Delta': delta, 'Gamma': gamma, 'Theta': theta, 'Vega': vega}

# Test the function
try:
    greeks = calculate_greeks('Call', 100, 100, 1, 0.2, 0.05)
    print("Delta:", greeks['Delta'])
    print("Gamma:", greeks['Gamma'])
    print("Theta:", greeks['Theta'])
    print("Vega:", greeks['Vega'])
except ValueError as e:
    print(e)
