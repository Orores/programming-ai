#!/bin/bash

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run unit tests
echo "Running unit tests..."
if ! python -m unittest discover tests; then
    echo "Unit tests failed."
    # Deactivate virtual environment before exiting due to failure
    deactivate
    exit 1
fi
echo "All unit tests passed."

# Deactivate virtual environment after running tests
echo "Deactivating virtual environment..."
deactivate
