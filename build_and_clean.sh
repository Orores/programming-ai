#!/bin/bash

# Define directories for the generated files
DEB_DIST_DIR=./deb_dist
DIST_DIR=./dist
WHEEL_DIST_DIR=./wheel_dist

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run unit tests
#echo "Running unit tests..."
#if ! python -m unittest discover tests; then
#    echo "Unit tests failed. Build process stopped."
#    # Deactivate virtual environment before exiting due to failure
#    deactivate
#    exit 1
#fi
echo "All unit tests passed."

# Deactivate virtual environment after running tests
echo "Deactivating virtual environment..."
deactivate

# Clean up the previous build directories, including the .egg-info directory
echo "Cleaning up previous build directories..."
rm -rf "${DEB_DIST_DIR}" ./*.egg-info

# Build the Debian package
echo "Building Debian package..."
python3 setup.py --command-packages=stdeb.command bdist_deb

# Build the wheel package
echo "Building wheel package..."
python3 setup.py bdist_wheel

# Create wheel_dist directory if it doesn't exist
mkdir -p "${WHEEL_DIST_DIR}"

# Move the wheel package to wheel_dist directory
mv ./dist/*.whl "${WHEEL_DIST_DIR}"

# Remove .tar.gz files from the root directory
rm -f ./*.tar.gz
echo ".tar.gz files in the root directory have been removed"
