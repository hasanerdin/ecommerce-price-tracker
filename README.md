🛒 E-Commerce Price & Discount Tracker
This project tracks product prices from online e-commerce platforms and stores historical pricing data to help users analyze price changes over time.
By providing simple and meaningful visualizations, the application enables users to understand price trends, identify discount periods, and make informed purchasing or pricing decisions.

🎯 Motivation
Product prices on online shopping platforms frequently change due to discounts, campaigns, and market dynamics. These changes are often temporary and difficult to track manually.
This project aims to provide an automated and transparent way to monitor historical price movements, allowing users to better understand pricing behavior over time.

👥 Target Users
- End users who want to identify the best time to purchase products
- Analysts interested in price trend analysis
- Businesses seeking insights into market price movements

🧩 User Stories
- As a user, I want to analyze historical price fluctuations of products so that I can identify the best time to purchase them.
- As a user, I want to visualize price changes over time using simple and meaningful charts to better understand pricing trends.

🚀 MVP Scope
The Minimum Viable Product (MVP) focuses on:
- Collecting product price data via API or web scraping
- Storing historical prices in a relational database
- Allowing users to filter products and time ranges
- Displaying clear, time-based price visualizations

The MVP intentionally excludes advanced features such as predictions, alerts, and competitor analysis to maintain a focused and maintainable scope.

🏗️ System Architecture
The application follows a modular, end-to-end data pipeline architecture:

```
Data Source (API / Scraping)
        ↓
Data Ingestion & Cleaning (Pandas)
        ↓
Relational Database (MySQL)
        ↓
Backend API (FastAPI / Flask)
        ↓
Frontend Dashboard (Streamlit)
        ↓
Public Deployment (Streamlit Cloud)
```

This separation ensures scalability, maintainability, and clear responsibility between components.

🗂️ Project Structure (Planned)

```
ecommerce-price-tracker/
├── data/
│   ├── raw/
│   └── processed/
├── ingestion/
│   └── fetch_prices.py
├── database/
│   ├── schema.sql
│   └── procedures.sql
├── backend/
│   └── main.py
├── frontend/
│   └── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

🛠️ Technologies Used
- Python
- Pandas
- MySQL
- FastAPI / Flask
- Streamlit
- REST APIs / Web Scraping
- Streamlit Cloud (Deployment)

🔒 Configuration & Security
Sensitive information such as API keys and database credentials is managed using environment variables and is not committed to the repository.

🌱 Future Improvements
- Price change notifications and alerts
- Competitor price comparison
- Market-level price volatility analysis
- Predictive models for price trend forecasting

📌 Status
This project is actively under development as part of a structured, time-boxed learning roadmap focused on building end-to-end data applications.

👤 Author
Hasan Erdin
GitHub: https://github.com/hasanerdin
LinkedIn: https://www.linkedin.com/in/hasanerdin