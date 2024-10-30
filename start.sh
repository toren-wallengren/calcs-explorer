#!/bin/bash

# Function to check Python version
check_python_version() {
  version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
  if [[ $(echo -e "$version\n3.10" | sort -V | head -n1) == "3.10" ]]; then
    return 0
  else
    return 1
  fi
}

# Check if the virtual environment directory exists
if [ ! -d "pycalcs" ]; then
  echo "Creating virtual environment with Python 3.12..."
  python3.12 -m venv pycalcs
  source pycalcs/bin/activate
  echo "Installing requirements..."
  pip install -r requirements.txt
else
  source pycalcs/bin/activate
  if ! check_python_version; then
    echo "Upgrading virtual environment to Python 3.12..."
    deactivate
    rm -rf pycalcs
    python3.12 -m venv pycalcs
    source pycalcs/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
  else
    echo "Virtual environment already exists with a compatible Python version."
  fi
fi

# Start Jupyter Lab
echo "Starting Jupyter Lab..."
jupyter lab