import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍬",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

div[data-testid="metric-container"]{
    background-color:#F8F9FA;
    border:2px solid #E6E6E6;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.10);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🍬 Nassau Candy")

st.sidebar.markdown("""
### Business Intelligence Dashboard

Developed using:

- 🐍 Python
- 📊 Streamlit
- 📈 Plotly
- 🗂️ Pandas
- 🗺️ Folium Maps
""")

st.sidebar.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("Nassau_Candy_Cleaned.csv")

# =====================================================
# TITLE
# =====================================================

st.title("🍬 Nassau Candy Profitability Dashboard")

st.markdown("""
### Interactive Business Intelligence Dashboard

Welcome to the **Nassau Candy Profitability Dashboard**.

This dashboard provides interactive insights into:

- 📈 Sales Performance
- 💰 Product Profitability
- 🏢 Division Performance
- 📉 Cost Diagnostics
- 📊 Pareto Analysis
- 🏭 Factory Location Analysis
""")

# =====================================================
# KPI CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📦 Products",
        df["Product Name"].nunique()
    )

with c2:
    st.metric(
        "🏢 Divisions",
        df["Division"].nunique()
    )

with c3:
    st.metric(
        "💰 Total Sales",
        f"${df['Sales'].sum():,.0f}"
    )

with c4:
    st.metric(
        "📈 Avg Margin",
        f"{df['Gross Margin %'].mean():.2f}%"
    )

st.markdown("---")

# =====================================================
# DASHBOARD MODULES
# =====================================================

st.subheader("📊 Dashboard Modules")

left, right = st.columns(2)

with left:

    st.success("""
### 📊 Executive Overview

✔ Revenue Summary

✔ Gross Profit Analysis

✔ Margin Analysis

✔ KPI Dashboard
""")

    st.success("""
### 💰 Product Profitability

✔ Top Products

✔ Profit Contribution

✔ Product Leaderboard

✔ Business Insights
""")

    st.success("""
### 🏢 Division Performance

✔ Revenue by Division

✔ Margin Distribution

✔ Profit Analysis

✔ Executive Summary
""")

with right:

    st.success("""
### 📉 Cost Diagnostics

✔ Cost vs Margin Analysis

✔ High Cost Products

✔ Low Margin Products

✔ Cost Optimization
""")

    st.success("""
### 📈 Pareto Analysis

✔ 80/20 Rule

✔ Cumulative Profit

✔ Top Products

✔ Pareto Leaderboard
""")

    st.success("""
### 🏭 Factory Locations

✔ Interactive Factory Map

✔ Factory Coordinates

✔ Product–Factory Mapping

✔ Geographic Insights
""")

st.markdown("---")

# =====================================================
# HOW TO USE
# =====================================================

st.subheader("🚀 How to Use")

st.info("""
1️⃣ Select a dashboard page from the **Pages** section in the left sidebar.

2️⃣ Apply interactive filters such as Date Range, Division, Margin Threshold and Product Search.

3️⃣ Explore KPIs, charts and business insights.

4️⃣ Open the **Factory Locations** page to visualize manufacturing locations on the interactive map.

5️⃣ Use the dashboard insights for better business decision-making.
""")

st.markdown("---")

# =====================================================
# PROJECT INFORMATION
# =====================================================

st.subheader("📌 Project Information")

st.write("**Project Name:** Nassau Candy Profitability Dashboard")

st.write("**Dataset:** Nassau Candy Cleaned Dataset")

st.write("**Tools Used:** Python, Streamlit, Pandas, Plotly, Folium")

st.write("**Modules Included:**")
st.write("- 📊 Executive Overview")
st.write("- 💰 Product Profitability")
st.write("- 🏢 Division Performance")
st.write("- 📉 Cost Diagnostics")
st.write("- 📈 Pareto Analysis")
st.write("- 🏭 Factory Locations")

st.write("**Objective:** Build an interactive Business Intelligence dashboard to analyze sales, profitability, manufacturing locations and business performance.")

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
<center>

<h4>🍬 Nassau Candy Profitability Dashboard</h4>

Developed by <b>Sonal Pada</b>

Data Analytics Project | Unified Mentor Pvt. Ltd.

</center>
""",
unsafe_allow_html=True
)