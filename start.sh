#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "pycalcs" ]; then
  echo "Creating virtual environment..."
  python3 -m venv pycalcs
  source pycalcs/bin/activate
  echo "Installing requirements..."
  pip install -r requirements.txt
else
  echo "Virtual environment already exists."
  source pycalcs/bin/activate
fi

# Start Jupyter Lab
echo "Starting Jupyter Lab..."
jupyter lab