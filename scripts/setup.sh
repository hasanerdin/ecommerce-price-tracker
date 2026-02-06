#!/bin/bash

# E-commerce Price Tracker - Project Setup Script

echo "=========================================="
echo "E-commerce Price Tracker - Setup"
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
echo ""
echo "Activating virtual environment..."
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
    echo "⚠️  Please edit .env with your DATABASE_URL and other secrets"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="

echo ""
echo "Next steps:"
echo "1. Edit .env file and set DATABASE_URL (Supabase Postgres)"
echo "2. Initialize database tables:"
echo "   python scripts/init_db.py"
echo "3. Seed predefined events:"
echo "   python backend/ingestion/seed_events.py"
echo "4. Run daily ingestion manually (optional):"
echo "   python backend/ingestion/daily_ingestion.py"
echo "5. Start FastAPI backend:"
echo "   uvicorn backend.main:app --reload"
echo ""
