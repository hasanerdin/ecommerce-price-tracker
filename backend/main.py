"""FastAPI application main entry point"""
from datetime import datetime, timezone
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import engine

from scripts.setup_database import setup_database
from backend.ingestion.daily_ingestion import run_daily_ingestion
from backend.schemas import HealthResponse
from backend.api.products.routes import router as product_router
from backend.api.analytics.routes import router as analytic_router
from backend.api.events.routes import router as event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    # Startup
    print("[STARTUP] Initializing database...")
    setup_database()
    yield
    # Shutdown
    print("[SHUTDOWN] Application shutting down...")

# Create FastAPI app
app = FastAPI(
    title="E-Commerce Price Tracker",
    description="Backend API for product price tracker",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
# app.include_router(event_router)
app.include_router(product_router)
app.include_router(analytic_router)
app.include_router(event_router)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint"""
    return {
        "message": "E-Commerce Price Tracker",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    from sqlalchemy import text

    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        timestamp=datetime.now(timezone.utc),
        database=db_status
    )

if __name__ == "__main__":
    import uvicorn
    from shared.config import get_settings

    settings = get_settings()
    uvicorn.run(
        "backend.main::app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )