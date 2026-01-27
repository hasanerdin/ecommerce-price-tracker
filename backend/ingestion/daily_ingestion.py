
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Product, PriceHistory
from backend.schemas import ProductCreate, PriceHistoryCreate
from backend.api.products import crud as product_crud
from backend.ingestion.fetch_products import fetch_all_products
from backend.ingestion.price_engine import generate_daily_price
from shared.constants import PriceType

PRICING_MODE = PriceType.Synthetic

def generate_product_create_data(product_data: dict) -> ProductCreate:
    return ProductCreate(
        extarnal_id=product_data["id"],
        title=product_data["title"],
        description=product_data["description"],
        base_price=product_data["price"],
        rating=product_data["rating"]["rate"],
    )

def generate_price_history_create_data(product: Product, final_price: float, metadata: dict) -> PriceHistoryCreate:    
    return PriceHistoryCreate(
        product_id=product.product_id,
        event_id= metadata["event_id"],
        price=final_price,
        price_change_reason=metadata["adjustment_reason"],
        price_source=metadata["price_source"].value,
        recorded_date=metadata["recorded_date"],
    )

def get_or_create_product(db: Session, product_data: dict) -> Product:
    product = product_crud.get_product_by_external_id(db, product_data["id"])
    if product is None:
        product_create_data = generate_product_create_data(product_data)
        product = product_crud.create_product(db, product_create_data)
    
    return product

def is_price_history_created(db: Session, product_id: int, recorded_date: date):
    price_history = product_crud.get_price_history_by_recorded_date(db, 
                                                                    product_id, 
                                                                    recorded_date)
    return price_history is not None

def run_daily_ingestion(db: Session, snapshot_date: Optional[date] = None) -> None:
    """
    Main daily ingestion routine
    """
    snapshot_date = snapshot_date or date.today()
    products = fetch_all_products()

    inserted_snapshots = 0

    try:
        for product_data in products:
            product = get_or_create_product(db, product_data)

            final_price, metadata = generate_daily_price(
                base_price=product.base_price,
                current_date=snapshot_date,
                pricing_mode=PRICING_MODE
            )            

            if is_price_history_created(db, product.product_id, snapshot_date):
                continue

            metadata["recorded_date"] = snapshot_date
            price_history_create_data = generate_price_history_create_data(product, final_price, metadata)
            
            product_crud.create_price_history(db, price_history_create_data)
            inserted_snapshots += 1

        print(f"[INGESTION] {inserted_snapshots} price snapshots inserted.")

    except Exception as e:
        db.rollback()
        raise e
    

if __name__ == "__main__":
    db: Session = get_db()
    snapshot_date = date.today()

    run_daily_ingestion(db, snapshot_date)
