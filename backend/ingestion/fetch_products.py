"""Fetch product price data from API"""
import requests 

from shared.config import get_product_api

product_api = get_product_api()

def fetch_all_products() -> dict:
    response = requests.get(product_api.api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise response.raise_for_status()