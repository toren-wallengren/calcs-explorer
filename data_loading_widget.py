# data_loading_widget.py

import ipywidgets as widgets
from IPython.display import display, clear_output
from data_loading import load_npv_data  # Assuming load_npv_data is defined in data_loading.py

# Create widgets for user inputs
csv_name_widget = widgets.Text(
    value='cashflows.csv',
    description='CSV Name:',
    placeholder='Enter CSV file name'
)

npv_type_widget = widgets.Dropdown(
    options=['annualized', 'deannualized', 'daily', 'custom'],
    value='annualized',
    description='NPV Type:'
)

custom_time_period_widget = widgets.IntText(
    value=365,
    description='Custom Time Period:',
    disabled=True
)

# Enable/disable the custom time period widget based on selected NPV type
def on_npv_type_change(change):
    custom_time_period_widget.disabled = (change['new'] != 'custom')

npv_type_widget.observe(on_npv_type_change, names='value')

# Button to load data
load_button = widgets.Button(description="Load Data")
output = widgets.Output()

# Function to load data based on widget inputs, with a callback to handle the loaded expression
def load_data(button, callback=None):
    with output:
        clear_output()
        csv_name = csv_name_widget.value
        npv_type = npv_type_widget.value
        custom_period = custom_time_period_widget.value if npv_type == 'custom' else None
        
        # Load NPV data from the CSV file
        npv_expr = load_npv_data(
            method="csv",
            file_path=csv_name,
            npv_type=npv_type,
            custom_scale=custom_period
        )
        
        # Display the loaded NPV expression
        print(f"Loaded NPV expression for {npv_type} type from {csv_name}.")
        if npv_type == 'custom':
            print(f"Custom time period: {custom_period} days")
        display(npv_expr)
        
        # Pass npv_expr to the callback if provided
        if callback:
            callback(npv_expr)

# Set button click handler
def set_load_button_callback(callback=None):
    load_button.on_click(lambda button: load_data(button, callback=callback))

# Function to display widgets in the notebook with a callback parameter
def display_data_loading_widget(callback=None):
    set_load_button_callback(callback)
    display(widgets.VBox([csv_name_widget, npv_type_widget, custom_time_period_widget, load_button, output]))
