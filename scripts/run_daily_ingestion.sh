#!/bin/bash
set -e

PROJECT_ROOT="/Users/hasanerdin/Documents/GitHub/ecommerce-price-tracker"
VENV_PATH="$PROJECT_ROOT/venv"
PYTHON="$VENV_PATH/bin/python"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/ingestion.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

cd "$PROJECT_ROOT" || exit 1

echo "[$(date)] Cron started" >> "$LOG_FILE"

$PYTHON backend/ingestion/daily_ingestion.py >> "$LOG_FILE" 2>&1

echo "[$(date)] Cron finished successfully" >> "$LOG_FILE"
