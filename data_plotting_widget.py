# data_plotting_widget.py

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
from sympy import lambdify, diff
from sympy.abc import r

# Create widgets for plot parameters
xmin_widget = widgets.FloatText(value=-1, description="X min:")
xmax_widget = widgets.FloatText(value=1, description="X max:")

xlog_widget = widgets.Checkbox(value=False, description="Log scale X")

steps_widget = widgets.IntSlider(value=100, min=10, max=1000, step=10, description="Steps")

# Button to trigger plotting
plot_button = widgets.Button(description="Plot Data")
output = widgets.Output()

# Function to generate x values based on widget input
def generate_x_values(xmin, xmax, steps, xlog):
    return np.logspace(xmin, xmax, steps) if xlog else np.linspace(xmin, xmax, steps)

# Function to calculate dynamic y-axis bounds with a scaling factor
def calculate_y_bounds(y_values):
    ymin, ymax = min(y_values), max(y_values)
    diff_y = ymax - ymin
    return ymin - 0.1 * diff_y, ymax + 0.1 * diff_y

# Plotting functions for each type of plot
def plot_npv(x_values, y_values, xlog):
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, label="NPV", color="blue")
    if xlog:
        plt.xscale('log')
    ymin, ymax = calculate_y_bounds(y_values)
    plt.xlim(x_values[0], x_values[-1])
    plt.ylim(ymin, ymax)
    plt.xlabel("Rate of Return (r)")
    plt.ylabel("Net Present Value (NPV)")
    plt.title("NPV as a Function of Rate of Return (r)")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_npv_derivative(x_values, y_derivative_values, xlog):
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_derivative_values, label="NPV Derivative", color="red")
    if xlog:
        plt.xscale('log')
    ymin, ymax = calculate_y_bounds(y_derivative_values)
    plt.xlim(x_values[0], x_values[-1])
    plt.ylim(ymin, ymax)
    plt.xlabel("Rate of Return (r)")
    plt.ylabel("Derivative of NPV")
    plt.title("Derivative of NPV as a Function of Rate of Return (r)")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_newton_iter(x_values, y_iter_values, xlog):
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_iter_values, label="Newton Iterating Function", color="green")
    if xlog:
        plt.xscale('log')
    ymin, ymax = calculate_y_bounds(y_iter_values)
    plt.xlim(x_values[0], x_values[-1])
    plt.ylim(ymin, ymax)
    plt.xlabel("Rate of Return (r)")
    plt.ylabel("Iterating Function for Newton's Method")
    plt.title("Newton Iterating Function as a Function of Rate of Return (r)")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_newton_iter_derivative(x_values, y_iter_derivative_values, xlog):
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_iter_derivative_values, label="Derivative of Newton Iterating Function", color="purple")
    if xlog:
        plt.xscale('log')
    ymin, ymax = calculate_y_bounds(y_iter_derivative_values)
    plt.xlim(x_values[0], x_values[-1])
    plt.ylim(ymin, ymax)
    plt.xlabel("Rate of Return (r)")
    plt.ylabel("Derivative of Iterating Function")
    plt.title("Derivative of Newton Iterating Function as a Function of Rate of Return (r)")
    plt.grid(True)
    plt.legend()
    plt.show()

# Main plot function that uses the individual plot functions
def plot_data(button, npv_expr=None, plots_to_show=["npv", "npv_derivative", "newton_iter", "newton_iter_derivative"]):
    if npv_expr is None:
        with output:
            clear_output()
            print("Error: NPV expression is not defined.")
        return
    
    with output:
        clear_output()
        
        # Retrieve widget values
        xmin = xmin_widget.value
        xmax = xmax_widget.value
        xlog = xlog_widget.value
        steps = steps_widget.value

        # Convert the symbolic npv_expr and its derivatives to numerical functions
        npv_function = lambdify(r, npv_expr, modules="numpy")
        npv_derivative_expr = diff(npv_expr, r)
        npv_derivative_function = lambdify(r, npv_derivative_expr, modules="numpy")
        npv_double_derivative_expr = diff(npv_derivative_expr, r)
        npv_double_derivative_function = lambdify(r, npv_double_derivative_expr, modules="numpy")
        
        # Define the Newton iterating function and its derivative
        def newton_iter_function(x):
            return x - npv_function(x) / npv_derivative_function(x)
        
        def newton_iter_derivative_function(x):
            f_prime = npv_derivative_function(x)
            f_double_prime = npv_double_derivative_function(x)
            return 1 - (f_prime * f_prime - npv_function(x) * f_double_prime) / (f_prime ** 2)
        
        # Generate x values
        x_values = generate_x_values(xmin, xmax, steps, xlog)
        
        # Plot based on specified types
        if "npv" in plots_to_show:
            y_values = npv_function(x_values)
            plot_npv(x_values, y_values, xlog)

        if "npv_derivative" in plots_to_show:
            y_derivative_values = npv_derivative_function(x_values)
            plot_npv_derivative(x_values, y_derivative_values, xlog)

        if "newton_iter" in plots_to_show:
            y_iter_values = newton_iter_function(x_values)
            plot_newton_iter(x_values, y_iter_values, xlog)
        
        if "newton_iter_derivative" in plots_to_show:
            y_iter_derivative_values = newton_iter_derivative_function(x_values)
            plot_newton_iter_derivative(x_values, y_iter_derivative_values, xlog)

# Set button click handler
def set_plot_button(npv_expr=None, plots_to_show=["npv", "npv_derivative", "newton_iter", "newton_iter_derivative"]):
    plot_button.on_click(lambda button: plot_data(button, npv_expr=npv_expr, plots_to_show=plots_to_show))

# Function to display plotting widgets in the notebook
def display_data_plotting_widget(npv_expr=None, plots_to_show=["npv", "npv_derivative", "newton_iter", "newton_iter_derivative"]):
    if npv_expr is None:
        print("No NPV expression provided.")
    else:
        set_plot_button(npv_expr=npv_expr, plots_to_show=plots_to_show)
        display(widgets.VBox([xmin_widget, xmax_widget, xlog_widget, steps_widget, plot_button, output]))
