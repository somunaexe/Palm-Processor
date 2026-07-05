import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=30000)  # refresh every 30 seconds
st.set_page_config(page_title="Palm Pro Dashboard", layout="wide")

API_URL = "http://backend:8000/events/latest"

# -----------------------
# DATA LOADING
# -----------------------
@st.cache_data(ttl=10)
def load_data():
    res = requests.get(API_URL)
    return pd.DataFrame(res.json())

df = load_data()
st.write(df.columns)
st.write(df.head())

if df.empty or "risk_score" not in df.columns:
    st.warning("No data yet — waiting for events...")
    st.stop()
# -----------------------
# HEADER
# -----------------------
st.title("📊 Palm Pro – Real-Time Sensor Intelligence Dashboard")

st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")

# -----------------------
# KPIs (TOP METRICS)
# -----------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Events", len(df))

with col2:
    avg_risk = df["risk_score"].mean()
    st.metric("Avg Risk Score", f"{avg_risk:.2f}")

with col3:
    high_risk = len(df[df["risk_score"] > 0.7])
    st.metric("High Risk Events", high_risk)

# -----------------------
# RISK DISTRIBUTION
# -----------------------
st.subheader("📈 Risk Score Distribution")

fig = px.histogram(
    df,
    x="risk_score",
    nbins=20,
    title="Distribution of Machine Risk"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# MACHINE STATUS VIEW
# -----------------------
st.subheader("🟢 Machine Health Overview")

df["status"] = df["risk_score"].apply(
    lambda x: "CRITICAL" if x > 0.8 else ("WARNING" if x > 0.5 else "OK")
)

status_counts = df["status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]

fig2 = px.pie(
    status_counts,
    names="status",
    values="count",
    title="System Health Breakdown"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# LIVE EVENT TABLE
# -----------------------
st.subheader("📡 Live Sensor Feed")

st.dataframe(
    df.sort_values(by="risk_score", ascending=False),
    use_container_width=True
)

# -----------------------
# ALERT PANEL
# -----------------------
st.subheader("🚨 Active Alerts")

alerts = df[df["risk_score"] > 0.7]

if len(alerts) == 0:
    st.success("No active alerts 🎉 System stable")
else:
    st.error(f"{len(alerts)} high-risk events detected!")

    st.dataframe(alerts)