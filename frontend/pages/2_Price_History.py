from datetime import timedelta
import streamlit as st
import pandas as pd
import plotly.express as px

from services.api_client import get_products, get_events, get_price_summary, get_product_price_history

st.title("📦 Price History")

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

start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date", value=None)

# ---------- Price History Chart ----------
st.subheader("📈 Price History")

history = get_product_price_history(product_id, start_date, end_date)
if not history:
    st.warning("No price history found.")
    st.stop()

events = get_events()
events_df = pd.DataFrame(events)
events_df["start_date"] = pd.to_datetime(events_df["start_date"])
events_df["end_date"] = pd.to_datetime(events_df["end_date"])

df = pd.DataFrame(history).merge(events_df, on="event_id", how="left")
df["recorded_date"] = pd.to_datetime(df["recorded_date"])
df = df.sort_values("recorded_date")

# Event Flag
df["is_event"] = df["event_name"].notnull()

padding = (df["price"].max() - df["price"].min()) * 0.1
fig = px.line(
    df,
    x="recorded_date",
    y="price",
    title="Price History",
    #markers=True,
    range_y=[
        df["price"].min() - padding, 
        df["price"].max() + padding
        ]
)

# --- Add vertical lines for events --- 
for _, row in events_df.iterrows():
    if row["start_date"] == row["end_date"]:
        fig.add_vline(
            x=row["start_date"],
            line_dash="dot",
            line_color="red",
        )
    else:
        fig.add_vrect(
            x0=row["start_date"],
            x1=row["end_date"],
            fillcolor="red",
            opacity=0.2,
            line_width=0
        )

    fig.add_annotation(
        x=row["start_date"] + (row["end_date"] - row["start_date"]) / 2,
        y=df["price"].max(),
        text=row["event_name"],
        showarrow=False,
        font=dict(size=10, color="white"),
        yshift=10,
    )

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified"
)

st.plotly_chart(fig, width="stretch")