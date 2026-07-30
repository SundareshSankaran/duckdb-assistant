#!/usr/bin/env bash

set -euo pipefail


# Parameters:
# 1 = name of virtual environment
# 2 = future use, path to requirements.txt (if different from default)

# Create a virtual environment
python -m venv $1

# Activate virtual environment
. $1/bin/activate

# upgrade pip to latest
python -m pip cache purge
python -m pip install --upgrade pip

# install uv for faster installation
python -m pip install --upgrade uv

# Install helper requirements
python -m uv pip install -r requirements.txt

# Install this package
cd .. && python -m pip install --upgrade -e .

echo "---------------------------------------------"
echo "Package installed in virtual environment $1"
echo "---------------------------------------------"