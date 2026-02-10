import streamlit as st
import pandas as pd
import plotly.express as px

from services.api_client import (
    get_products,
    get_events,
    get_event_impact
)

st.set_page_config(page_title="Event Impact", layout="wide")

st.title("🎯 Event Impact Analysis")
st.caption("Analyze how discount events affect product prices")

# -------------------------------
# Load data
# -------------------------------
products = get_products()
events = get_events()

if not products or not events:
    st.warning("Products or events not found.")
    st.stop()

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.header("Filters")

product_map = {f"{p['title']}": p for p in products}
event_map = {e["event_name"]: e for e in events}

selected_product_name = st.sidebar.selectbox(
    "Select Product",
    product_map.keys()
)

selected_event_name = st.sidebar.selectbox(
    "Select Event",
    event_map.keys()
)

product_id = product_map[selected_product_name]["product_id"]
event_id = event_map[selected_event_name]["event_id"]

# -------------------------------
# Fetch impact data
# -------------------------------
with st.spinner("Calculating event impact..."):
    impact = get_event_impact(product_id, event_id)

# -------------------------------
# Metrics
# -------------------------------
st.subheader(f"📌 {impact['event_name']}")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Pre-Event Avg Price",
    f"{impact['pre_event_avg_price']}"
)

c2.metric(
    "Event Avg Price",
    f"{impact['event_avg_price']}",
    delta=f"{impact['pre_to_event_percentage_change']}%"
)

c3.metric(
    "Post-Event Avg Price",
    f"{impact['post_event_avg_price'] or 'N/A'}",
    delta=f"{impact['event_to_post_percentage_change']}%"
    if impact['event_to_post_percentage_change'] else None
)

# -------------------------------
# Visualization
# -------------------------------
st.subheader("📊 Price Comparison")

df = pd.DataFrame({
    "Period": ["Pre-Event", "Event", "Post-Event"],
    "Average Price": [
        impact["pre_event_avg_price"],
        impact["event_avg_price"],
        impact["post_event_avg_price"]
    ]
})

fig = px.bar(
    df,
    x="Period",
    y="Average Price",
    text="Average Price",
    title="Average Price by Period"
)

fig.update_traces(textposition="outside")
fig.update_layout(yaxis_title="Price")

st.plotly_chart(fig, use_container_width=True)
