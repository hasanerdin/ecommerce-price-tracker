#!/bin/bash

# AI Trip Planner - Project Setup Script

echo "=========================================="
echo "AI Trip Planner - Project Setup"
echo "=========================================="

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your MySQL credentials and API keys"
fi

# Check MySQL connection
echo ""
echo "Checking MySQL connection..."
echo "⚠️  Make sure MySQL is running on localhost:3306"
echo "⚠️  Create database 'price-tracker' if it doesn't exist:"
echo "    mysql -u root -p -e 'CREATE DATABASE IF NOT EXISTS price-tracker;'"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Create MySQL database: CREATE DATABASE price-tracker;"
echo "3. Run: python scripts/setup_database.py"
echo "4. Run: python scripts/load_sample_data.py"
echo "5. Start backend: bash scripts/run_backend.sh"
echo ""
