import requests
from typing import List, Dict, Optional
from datetime import date
import os

# BASE_API_URL = "http://localhost:8000"
BASE_API_URL = os.getenv("API_BASE_URL")


def check_api_health() -> bool:
    try:
        response = requests.get(f"{BASE_API_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_products() -> List[Dict]:
    response = requests.get(f"{BASE_API_URL}/products")
    response.raise_for_status()
    return response.json()

def get_events() -> List[Dict]:
    response = requests.get(f"{BASE_API_URL}/events")
    response.raise_for_status()
    return response.json()

def get_product_price_history(
    product_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[Dict]:
    params = {
        "product_id": product_id,
        "start_date": start_date,
        "end_date": end_date,
    }
    response = requests.get(f"{BASE_API_URL}/analytics/price-history", params=params)
    response.raise_for_status()
    return response.json()

def get_price_summary(
        product_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
) -> Dict[str, float]:
    params = {
        "product_id": product_id,
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(f"{BASE_API_URL}/analytics/price-summary", params=params)
    response.raise_for_status()
    return response.json()

def get_event_impact(product_id: int, event_id: int) -> dict:
    params = {
        "product_id": product_id,
        "event_id": event_id
    }
    response = requests.get(f"{BASE_API_URL}/analytics/event-impact", params=params)
    response.raise_for_status()
    return response.json()