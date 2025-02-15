import numpy as np
import time

def binomial_option_price(
    option_type='call',         # 'call' or 'put'
    exercise_type='European',   # 'European' or 'American'
    S0=100,                     # Initial stock price
    K=110,                      # Strike price
    T=1,                        # Time to expiry (years)
    r=0.05,                     # Risk-free interest rate (annualized)
    sigma=0.2,                  # Volatility or percentage move if fixed_moves=True
    steps=100,                  # Number of binomial steps
    fixed_moves=False,          # If True, use fixed moves: u=1+sigma, d=1-sigma
    u=None,                     # Up factor (if provided, overrides calculation)
    d=None                      # Down factor (if provided, overrides calculation)
):
    start_time = time.time()
    dt = T / steps
    
    # Compute up/down factors
    if fixed_moves:
        if u is None:
            u = 1 + sigma
        if d is None:
            d = 1 - sigma
    else:
        if u is None:
            u = np.exp(sigma * np.sqrt(dt))
        if d is None:
            d = 1 / u
    
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability
    discount = np.exp(-r * dt)  # Discount factor per step
    
    # Compute terminal stock prices at maturity (step N)
    j = np.arange(steps + 1)  # Indices for all possible nodes
    stock_prices = S0 * (u ** (steps - j)) * (d ** j)
    #print(j)
    #print(stock_prices)
    
    # Compute terminal option values (intrinsic payoff)
    if option_type == 'call':
        option_values = np.maximum(0, stock_prices - K)
    else:
        option_values = np.maximum(0, K - stock_prices)
    
    # Backward induction to determine option price at t=0
    for i in range(steps - 1, -1, -1):
        option_values = discount * (p * option_values[:-1] + (1 - p) * option_values[1:])
        if exercise_type == 'American':
            stock_prices = stock_prices[:-1] / u  # Backward stock price update
            #print(stock_prices)
            if option_type == 'call':
                #print(option_values)
                option_values = np.maximum(option_values, stock_prices - K)
            else:
                #print(option_values)
                option_values = np.maximum(option_values, K - stock_prices)
    
    computation_time = time.time() - start_time
    num_paths = (steps + 1) * (steps + 2) // 2  # Total nodes in the tree
    #print(option_values)
    
    return option_values[0], computation_time, num_paths

# Example run for the case where each move is fixed at 10% (u=1.1, d=0.9)
price, time_taken, paths = binomial_option_price(
    option_type='call',
    exercise_type='American',
    S0=20,
    K=21,
    T=0.5,
    r=0.12,
    sigma=0.1,    # 10% move per step
    steps=2,
    fixed_moves=True  # Use fixed moves rather than CRR calculation
)

print(f"Option Price: {price:.4f}, Computation Time: {time_taken:.6f} sec, Number of Paths: {paths}")

price, time_taken, paths = binomial_option_price(
    option_type='put',
    exercise_type='American',
    S0=50,
    K=52,
    T=2,
    r=0.05,
    sigma=0.2,    # 20% move per step
    steps=2,
    fixed_moves=True  # Use fixed moves rather than CRR calculation
)

print(f"Option Price: {price:.4f}, Computation Time: {time_taken:.6f} sec, Number of Paths: {paths}")

price, time_taken, paths = binomial_option_price(
    option_type='put',
    exercise_type='American',
    S0=50,
    K=52,
    T=2,
    r=0.05,
    sigma=0.2,    # 20% move per step
    steps=1000,
    fixed_moves=False  # Use fixed moves rather than CRR calculation
)

print(f"Option Price: {price:.4f}, Computation Time: {time_taken:.6f} sec, Number of Paths: {paths}")

