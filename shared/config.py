"""Shared configuration settings"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database Configuration
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "price-tracker"
    db_user: str = "root"
    db_password: str = ""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Frontend Configuration
    frontend_port: int = 8501

    # API keys
    # TODO: If any API is required, add here

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """Construct MySQL database URL"""
        return f"Mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()