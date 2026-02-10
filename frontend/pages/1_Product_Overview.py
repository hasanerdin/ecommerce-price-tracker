import streamlit as st

from services.api_client import get_products, get_price_summary, get_product_price_history

st.title("📦 Product Overview")

# --- Sidebar ---
st.sidebar.header("🔎 Filters")

with st.spinner("Loading products..."):
    products = get_products()

if not products:
    st.warning("No products found.")
    st.stop()

product_map = {
    f"{p['title']} (ID: {p['product_id']})": p
    for p in products
}

selected_label = st.sidebar.selectbox(
    "Select a product",
    options=list(product_map.keys())
)

selected_product = product_map[selected_label]
product_id = selected_product["product_id"]

# --- Product info ---
st.subheader("🧾 Product Information")

c1, c2, _ = st.columns(3)
c1.metric("Base Price", f"{selected_product['base_price']}")
c2.metric("Rating", selected_product["rating"])

# --- Price summary ---
st.subheader("📊 Price Summary")

summary = get_price_summary(product_id)

if summary:
    c1, c2, c3 = st.columns(3)
    c1.metric("Min Price", f"{summary['min_price']:.2f}")
    c2.metric("Max Price", f"{summary['max_price']:.2f}")
    c3.metric("Avg Price", f"{summary['avg_price']:.2f}")
else:
    st.info("No price data available.")
