import streamlit as st
import pandas as pd

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)

# ==========================
# Title
# ==========================
st.title("📊 Executive Business Overview")

st.markdown("""
### Nassau Candy Sales, Profitability & Margin Performance Dashboard

Monitor business performance using interactive filters and key performance indicators.
""")

st.markdown("---")

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("Nassau_Candy_Cleaned.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# ==========================
# Sidebar Filters
# ==========================
st.sidebar.header("🔍 Dashboard Filters")

start_date = st.sidebar.date_input(
    "📅 Start Date",
    value=df["Order Date"].min()
)

end_date = st.sidebar.date_input(
    "📅 End Date",
    value=df["Order Date"].max()
)

division_list = ["All"] + sorted(df["Division"].unique())

selected_division = st.sidebar.selectbox(
    "🏢 Select Division",
    division_list
)

margin_threshold = st.sidebar.slider(
    "📈 Minimum Gross Margin (%)",
    0,
    100,
    0
)

product_search = st.sidebar.text_input(
    "🔎 Search Product"
)

# ==========================
# Apply Filters
# ==========================
filtered_df = df[
    (df["Order Date"] >= pd.Timestamp(start_date)) &
    (df["Order Date"] <= pd.Timestamp(end_date))
]

if selected_division != "All":
    filtered_df = filtered_df[
        filtered_df["Division"] == selected_division
    ]

filtered_df = filtered_df[
    filtered_df["Gross Margin %"] >= margin_threshold
]

if product_search:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(
            product_search,
            case=False,
            na=False
        )
    ]

# ==========================
# KPI Calculations
# ==========================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
avg_margin = filtered_df["Gross Margin %"].mean()
total_products = filtered_df["Product Name"].nunique()
total_divisions = filtered_df["Division"].nunique()

top_product = filtered_df.loc[
    filtered_df["Gross Profit"].idxmax(),
    "Product Name"
] if not filtered_df.empty else "N/A"

# ==========================
# KPI Cards
# ==========================
st.subheader("📈 Executive KPI Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("💰 Total Revenue", f"${total_sales:,.2f}")

with c2:
    st.metric("💵 Total Gross Profit", f"${total_profit:,.2f}")

with c3:
    st.metric("📈 Average Margin", f"{avg_margin:.2f}%")

c4, c5, c6 = st.columns(3)

with c4:
    st.metric("📦 Products", total_products)

with c5:
    st.metric("🏢 Active Divisions", total_divisions)

with c6:
    st.metric("🏆 Top Product", top_product)

st.markdown("---")

# ==========================
# Business Summary
# ==========================
st.subheader("📋 Executive Business Summary")

st.success(f"""
💰 **Total Revenue:** ${total_sales:,.2f}

💵 **Total Gross Profit:** ${total_profit:,.2f}

📈 **Average Gross Margin:** {avg_margin:.2f}%

📦 **Products Available:** {total_products}

🏢 **Business Divisions:** {total_divisions}

🏆 **Highest Profit Product:** {top_product}
""")

st.markdown("---")

st.info("""
### 💡 Business Insights

✅ Monitor high-margin products to maximize profitability.

✅ Use the filters on the left to analyze performance by date, division, margin and product.

✅ This dashboard provides an executive summary of Nassau Candy's overall business performance.
""")


