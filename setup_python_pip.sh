#!/bin/bash

# Step 1: Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    python3_version=$(python3 --version 2>&1)
    echo "Python 3 is already installed:"
    echo "Python 3 version: $python3_version"
else
    # Step 2: Install Python 3
    echo "Python 3 is not installed. Installing Python 3..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    elif [[ "$OSTYPE" == "linux-gnu" ]]; then
        sudo apt-get update
        sudo apt-get install python3
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "Please install Python 3 manually and re-run this script."
        exit 1
    else
        echo "Unsupported OS"
        exit 1
    fi
fi

# Step 3: Check if pip is installed
if command -v python3 -m pip &>/dev/null; then
    pip_version=$(python3 -m pip --version 2>&1)
    echo "pip is already installed and can be invoked as 'python3 -m pip':"
    echo "$pip_version"
else
    # Step 4: Install pip for Python 3
    echo "pip is not installed for Python 3. Installing pip for Python 3..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        python3 -m ensurepip --default-pip
    elif [[ "$OSTYPE" == "linux-gnu" ]]; then
        sudo apt-get install python3-pip
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        echo "Please install pip for Python 3 manually and re-run this script."
        exit 1
    else
        echo "Unsupported OS"
        exit 1
    fi
fi

echo "Python 3 and pip (python3 -m pip) are now installed and configured."

