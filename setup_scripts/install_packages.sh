#!/bin/bash

# Update system packages and install essential packages
echo "Updating system and installing required packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker and Python3 packages
echo "Installing Docker, Python3, and other dependencies..."
sudo apt install -y docker.io python3 python3-pip git

# Enable Docker without sudo (optional but recommended)
echo "Adding user to Docker group for non-sudo Docker usage..."
sudo usermod -aG docker $USER
echo "User added to Docker group. Please log out and log back in for the changes to take effect."

# Install Python dependencies
echo "Installing Python dependencies (mxnet, xgboost, numpy, pandas)..."
pip3 install mxnet xgboost numpy pandas

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version

# Verify Python installation
echo "Verifying Python installation..."
python3 --version
pip3 show mxnet xgboost numpy pandas

# Completion message
echo "Package installation completed successfully!"
