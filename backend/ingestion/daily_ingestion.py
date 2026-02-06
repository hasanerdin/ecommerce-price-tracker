
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Product, PriceHistory
from backend.schemas import ProductCreate, PriceHistoryCreate
from backend.ingestion.fetch_products import fetch_all_products
from backend.ingestion.price_engine import generate_daily_price
from shared.constants import PriceType

PRICING_MODE = PriceType.Synthetic

def get_product(db: Session, external_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.external_id == external_id).first()

def create_product(product_data: dict) -> Product:
    return Product(
        external_id=product_data["id"],
        title=product_data["title"],
        description=product_data["description"],
        base_price=product_data["price"],
        rating=product_data["rating"]["rate"]
    )

def is_price_history_created(db: Session, product_id: int, recorded_date: date) -> bool:
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.recorded_date == recorded_date
    ).first()

    return price_history is not None

def create_price_history(product: Product, final_price: float, metadata: dict) -> PriceHistory:
    return PriceHistory(
        product_id=product.product_id,
        event_id=metadata["event_id"],
        price=final_price,
        price_change_reason=metadata["adjustment_reason"],
        price_source=metadata["price_source"].value,
        recorded_date=metadata["recorded_date"]
    )

def run_daily_ingestion(snapshot_date: Optional[date] = None) -> None:
    """
    Main daily ingestion routine
    """
    db = SessionLocal()
    snapshot_date = snapshot_date or date.today()

    products = fetch_all_products()

    inserted_snapshots = 0
    try:
        for product_data in products:
            product = get_product(db, product_data["id"])
            if product is None:
                product = create_product(product_data)
                db.add(product)
                db.flush()

            final_price, metadata = generate_daily_price(
                db,
                base_price=product.base_price,
                current_date=snapshot_date,
                pricing_mode=PRICING_MODE
            )            

            if is_price_history_created(db, product.product_id, snapshot_date):
                continue

            price_history = create_price_history(product, final_price, metadata)
            
            db.add(price_history)
            inserted_snapshots += 1

        db.commit()
        print(f"[INGESTION] {inserted_snapshots} price snapshots inserted.")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_daily_ingestion()
