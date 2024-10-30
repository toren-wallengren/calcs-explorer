# data_loading.py
import pandas as pd
from sympy import symbols
from sympy.abc import r

def load_cashflows_from_csv(file_path, npv_type="deannualized", custom_scale=None):
    """
    Load cashflows from a CSV file and generate a symbolic NPV expression
    with the variable 'r' as the rate of return.

    Parameters:
        file_path (str): Path to the CSV file with 'Date' and 'Amount' columns.
        npv_type (str): Type of NPV scaling to use ('annualized', 'deannualized', 'daily', 'custom').
        custom_scale (int, optional): Custom scaling value, only used if npv_type is 'custom'.

    Returns:
        npv_expr (sympy expression): Symbolic NPV expression.
    """
    # Load data
    data = pd.read_csv(file_path, parse_dates=['Date'])
    data = data.sort_values(by='Date')
    data['Days'] = (data['Date'] - data['Date'].iloc[0]).dt.days
    
    # Determine the exponent scale based on npv_type
    if npv_type == "annualized":
        exponent_scale = 365
    elif npv_type == "deannualized":
        exponent_scale = data['Days'].iloc[-1]
    elif npv_type == "daily":
        exponent_scale = 1
    elif npv_type == "custom" and custom_scale is not None:
        exponent_scale = custom_scale
    else:
        raise ValueError("Invalid NPV type or missing custom scale for 'custom' NPV type.")
    
    # Create symbolic NPV expression
    npv_expr = sum(row.Amount / (1 + r)**(row.Days / exponent_scale) for row in data.itertuples())
    return npv_expr


def define_custom_npv_function(custom_expression_str, additional_params=None):
    """
    Define a custom NPV function with symbolic parameters.

    Parameters:
        custom_expression_str (str): The custom NPV function as a string.
        additional_params (list of str): List of additional parameters to include as symbols.

    Returns:
        npv_expr (sympy expression): Symbolic NPV expression with specified parameters.
    """
    # Define r and any additional symbolic parameters
    symbols_dict = {'r': r}
    if additional_params:
        for param in additional_params:
            symbols_dict[param] = symbols(param)
    
    # Parse custom NPV expression
    npv_expr = eval(custom_expression_str, {"__builtins__": None}, symbols_dict)
    
    return npv_expr


def load_npv_data(method, *args, **kwargs):
    """
    Load NPV data using the specified method (CSV or custom function).

    Parameters:
        method (str): Method for loading data ('csv' or 'custom').
        *args, **kwargs: Additional arguments for each method.

    Returns:
        npv_expr (sympy expression): Symbolic NPV expression.
    """
    if method == "csv":
        return load_cashflows_from_csv(*args, **kwargs)
    elif method == "custom":
        return define_custom_npv_function(*args, **kwargs)
    else:
        raise ValueError("Invalid method. Choose 'csv' or 'custom'.")
