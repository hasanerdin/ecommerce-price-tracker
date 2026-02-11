"""Shared configuration settings"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from shared.constants import PriceType

class Settings(BaseSettings):
    """Application settings for MySQL from environment variables"""
    # Database Configuration
    db_host: str = os.getenv("DB_HOST")
    db_port: int = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")

    model_config=SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    @property
    def database_url(self) -> str:
        """Construct MySQL database URL"""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

class ProductAPI:
    """API informations to fetch product's prices"""    
    url: str = "https://fakestoreapi.com"
    endpoint: str = "products"
    price_mode: str = PriceType.Synthetic

    @property
    def api_url(self) -> str:
        """Construct API URL"""
        return f"{self.url}/{self.endpoint}"
    
    @property
    def api_url_for_product(self, product_id: int) -> str:
        """Construct API URL for single product by ID"""
        return f"{self.api_url}/{product_id}"

@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

@lru_cache
def get_product_api() -> ProductAPI:
    """Get cached product api instance"""
    return ProductAPI()