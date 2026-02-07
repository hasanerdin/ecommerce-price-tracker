🛒 E-Commerce Price & Discount Tracker

An end-to-end backend system that tracks product prices from e-commerce platforms, simulates realistic price changes (discounts, campaigns, noise), and exposes analytical insights through a RESTful API.

The project focuses on clean data modeling, reliable ingestion, and event-based price analytics, serving as a strong backend foundation for future dashboards and data applications.

🎯 Motivation

Product prices in e-commerce platforms change frequently due to campaigns, seasonal events, and market behavior.
These changes are often temporary, unstructured, and hard to analyze retrospectively.

This project aims to:

- Automatically track product prices over time
- Store historical price snapshots in a structured database
- Simulate realistic pricing behavior (events, discounts, noise)
- Provide clean analytical endpoints to measure event impact on prices

👥 Target Users

- End users who want to analyze historical price trends
- Data analysts interested in pricing behavior and event impact
- Developers building dashboards or analytics on top of pricing data

🧩 User Stories

- As a user, I want to analyze historical price movements to understand pricing trends.
- As a user, I want to measure how discount events affect product prices.
- As an analyst, I want a clean API to retrieve price history and analytics.
- As a developer, I want a reusable backend that can power different frontends.

🚀 MVP Scope

The MVP intentionally focuses on backend robustness and data correctness.

Included:
- Product ingestion via API
- Daily price snapshot generation
- Event-based price adjustments (pre-event uplift, discounts)
- Historical price storage
- Analytical REST endpoints
- Unit and integration tests
- Scheduled ingestion via cron

Excluded (by design):
- Price prediction
- Notifications or alerts
- Competitor comparison
- Frontend dashboards (planned next)

🏗️ System Architecture

The application follows a modular, end-to-end data pipeline architecture:

```
E-commerce API
      ↓
Daily Ingestion Script (Python)
      ↓
Pricing Engine (Synthetic Price Logic)
      ↓
MySQL Database
      ↓
FastAPI Backend (Analytics & Data Access)
      ↓
(Planned) Streamlit Dashboard
```

The system is designed with clear separation of concerns:
- Ingestion logic
- Pricing rules
- Database access
- Analytics
- API layer

🗂️ Project Structure (Planned)

```
ecommerce-price-tracker/
├── backend/
│   ├── api/
│   │   ├── products/
│   │   |   ├── crud.py
│   │   |   └── routes.py
│   │   ├── events/
│   │   |   ├── crud.py
│   │   |   └── routes.py
│   │   └── analytics/
│   │       ├── crud.py
│   │       └── routes.py
│   ├── ingestion/
│   │   ├── fetch_products.py
│   │   ├── price_engine.py
│   │   ├── daily_ingestion.py
│   │   ├── seed_data.py
│   │   └── seed_events.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── main.py
│
├── scripts/
│   ├── run_daily_ingestion.py
│   ├── setup_database.py
│   └── setup.sh
│
├── shared/
│   ├── config.py
│   └── constants.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── pyproject.toml
├── .env
├── requirements.txt
└── README.md

```

🛠️ Tech Stack
- Python 3.10
- FastAPI – RESTful backend
- SQLAlchemy – ORM & database modeling
- Pydantic – schema validation
- MySQL – relational database
- Pytest – unit & integration testing
- Cron – scheduled daily ingestion

🔑 Key Backend Features

🔹 Daily Price Ingestion
- Fetches product data from API
- Generates synthetic daily prices
- Ensures idempotent ingestion (no duplicate daily records)

🔹 Pricing Engine
- Base-price anchored pricing (prevents price drift)
- Pre-event uplift simulation
- Event-day discount application
- Optional noise for realistic fluctuations

🔹 Event Modeling
- Discount events stored in database
- Pre-event and event periods handled explicitly
- Clean separation between baseline and event prices

🔹 Analytics Endpoints
- Price history per product
- Price summary (min / max / average)
- Event impact analysis (pre-event vs event)

🔌 API Overview (MVP)
Endpoint	                Description
GET /health	                Health check
GET /products	                List products
GET /prices/history	        Price time series
GET /analytics/price-summary	Min / Max / Avg prices
GET /analytics/event-impact	Measure event price impact
GET /events	                List discount events

🧪 Testing

The project includes:
- Unit tests for pricing logic and event rules
- Integration tests for ingestion workflows
- Idempotency checks for daily ingestion
- All tests must pass before ingestion or API changes.

🔒 Configuration & Security

Sensitive information such as API keys and database credentials is managed using environment variables and is not committed to the repository.

📌 Status

✅ Backend completed
🚧 Frontend (Streamlit dashboard) planned as next phase

🌱 Future Improvements

- Streamlit-based interactive dashboard
- Event comparison across products
- Volatility metrics
- Moving-average based pricing anchors
- ML-ready feature extraction layer

👤 Author

Hasan Erdin

GitHub: https://github.com/hasanerdin

LinkedIn: https://www.linkedin.com/in/hasanerdin
