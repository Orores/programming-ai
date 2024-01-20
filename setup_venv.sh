#!/bin/bash

# Step 1: Check if Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is not installed or not in your PATH."
    echo "Please install Python 3 and ensure it's in your PATH."
    exit 1
fi

# Step 2: Check if python3-venv package is installed and install if necessary
if ! dpkg -l | grep python3-venv &>/dev/null; then
    echo "Installing python3-venv package..."
    sudo apt-get -y install python3-venv
fi

# Step 4: Check if the venv folder already exists
if [ -d "venv" ]; then
    echo "The 'venv' folder already exists in this directory."
else
    # Step 5: Initialize the virtual environment
    python3 -m venv venv
    echo "Virtual environment 'venv' is set up."
fi

