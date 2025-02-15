# Binomial Tree Option Pricing

## Overview
This project implements a Python function to price European and American Call/Put options using the Binomial Tree model. The function allows flexibility in specifying the number of steps in the tree for greater accuracy.

## Features
- Supports both **Call** and **Put** options.
- Supports both **European** and **American** options.
- Flexible number of steps in the binomial tree.
- Computes:
  - **Option price**
  - **Time of computation**
  - **Number of paths considered**
  - **Supports fixed or computed up/down moves**

## Installation
Ensure you have Python 3 installed along with the necessary libraries:
```bash
pip install numpy
pip install time
```

## Function Signature
```python
import numpy as np
import time

def binomial_option_price(
    option_type='call',         # 'call' or 'put'
    exercise_type='European',   # 'European' or 'American'
    S0=100,                     # Initial stock price
    K=110,                      # Strike price
    T=1,                        # Time to expiry (years)
    r=0.05,                     # Risk-free interest rate (annualized)
    sigma=0.2,                  # Volatility
    steps=100,                  # Number of binomial steps
    fixed_moves=False,          # Use fixed moves (u=1+sigma, d=1-sigma)
    u=None,                     # Up factor (if provided)
    d=None                      # Down factor (if provided)
):
    """
    Prices a European/American Call/Put option using the binomial tree model.
    
    Parameters:
        option_type (str): 'call' or 'put' (default: 'call')
        exercise_type (str): 'European' or 'American' (default: 'European')
        S0 (float): Initial stock price
        K (float): Strike price of the option
        T (float): Time to expiry in years
        r (float): Risk-free interest rate (annualized)
        sigma (float): Volatility of the underlying asset
        steps (int): Number of steps in the binomial tree
        fixed_moves (bool): If True, use fixed up/down moves
        u (float, optional): Up factor override
        d (float, optional): Down factor override

    Returns:
        tuple: (option_price, computation_time, num_paths)
    """
```

## Usage Example
```python
# Import function
from binomial_option_pricer import binomial_option_price

# Price an American call option with fixed moves
price, comp_time, num_paths = binomial_option_price(
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

print(f"Option Price: {price:.4f}")
print(f"Computation Time: {comp_time:.6f} seconds")
print(f"Number of Paths Considered: {num_paths}")
```

## Performance Considerations
- Increasing `steps` improves accuracy but increases computation time.
- American options require additional checks at each node, making them slightly slower than European options.
- Using `fixed_moves=True` forces predefined up/down moves instead of computed values.

## License
This project is open-source and available under the MIT License.

