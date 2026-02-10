import streamlit as st
from services.api_client import check_api_health

st.set_page_config(
    page_title="E-Commerce Price & Discount Tracker",
    layout="wide"
)

st.title("🛒 E-Commerce Price & Discount Tracker")

st.markdown(
    """
    ### 📊 Project Overview

    This application tracks historical product prices from e-commerce platforms and helps users 
    analyze how prices change over time, especially around discount events such as campaigns or seasonal sales.

    The system automatically collects daily price snapshots, stores them in a database, 
    and provides analytical insights through interactive visualizations.

    ---
    ### 🎯 What You Can Do Here

    - 📦 **Explore Products**  
      Browse available products and inspect their pricing history.

    - 📈 **Analyze Price Trends**  
      Visualize how product prices evolve over time and identify meaningful patterns.

    - 🎉 **Measure Event Impact**  
      Compare prices before and during discount events to understand their real impact.

    ---
    ### 🧭 How to Use the App

    1. Use the **sidebar menu** to navigate between pages.
    2. Select a **product** and a **date range** where applicable.
    3. Explore interactive charts and analytics generated from real historical data.

    ---
    ### 🛠️ Technical Notes

    - The frontend is built with **Streamlit**
    - All data is fetched from a **FastAPI backend**
    - Pricing data is stored in a **MySQL database**
    - Prices include realistic simulations such as discounts, pre-event uplifts, and noise

    ---
    🚀 This project focuses on clean data modeling, reproducible ingestion, and meaningful analytics.
    """
)

st.info("⬅️ Use the sidebar to start exploring the application.")

if check_api_health():
    st.success("✅ Backend API is running")
else:
    st.error("❌ Backend API is not reachable")