import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Cost Diagnostics",
    page_icon="📉",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📉 Cost vs Margin Diagnostics")

st.markdown("""
### Analyze product costs and identify products affecting profitability.
""")

st.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("Nassau_Candy_Cleaned.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# =====================================================
# SIDEBAR FILTERS
# =====================================================

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

# =====================================================
# APPLY FILTERS
# =====================================================

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

if filtered_df.empty:
    st.warning("No records found.")
    st.stop()

# =====================================================
# KPI CARDS
# =====================================================

avg_cost = filtered_df["Cost"].mean()
avg_profit = filtered_df["Gross Profit"].mean()
avg_margin = filtered_df["Gross Margin %"].mean()
products = filtered_df["Product Name"].nunique()

st.subheader("📊 Cost Diagnostics Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💰 Average Cost", f"${avg_cost:,.2f}")

with c2:
    st.metric("💵 Average Profit", f"${avg_profit:,.2f}")

with c3:
    st.metric("📈 Average Margin", f"{avg_margin:.2f}%")

with c4:
    st.metric("📦 Products", products)

st.markdown("---")

# =====================================================
# COST VS MARGIN SCATTER
# =====================================================

scatter = px.scatter(
    filtered_df,
    x="Cost",
    y="Gross Margin %",
    size="Gross Profit",
    color="Division",
    hover_name="Product Name",
    title="🎯 Cost vs Gross Margin Analysis"
)

scatter.update_layout(height=550)

st.plotly_chart(
    scatter,
    use_container_width=True
)

# =====================================================
# HIGH COST PRODUCTS
# =====================================================

st.markdown("---")

st.subheader("🚩 Top 10 High Cost Products")

high_cost = filtered_df.sort_values(
    "Cost",
    ascending=False
).head(10)

st.dataframe(
    high_cost[
        [
            "Product Name",
            "Division",
            "Sales",
            "Cost",
            "Gross Profit",
            "Gross Margin %",
            "Profit Per Unit"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# =====================================================
# LOW MARGIN PRODUCTS
# =====================================================

st.markdown("---")

st.subheader("⚠️ Top 10 Low Margin Products")

low_margin = filtered_df.sort_values(
    "Gross Margin %",
    ascending=True
).head(10)

st.dataframe(
    low_margin[
        [
            "Product Name",
            "Division",
            "Gross Margin %",
            "Gross Profit",
            "Cost"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.markdown("---")

st.subheader("💡 Business Insights")

highest_cost_product = high_cost.iloc[0]["Product Name"]
highest_cost = high_cost.iloc[0]["Cost"]

lowest_margin_product = low_margin.iloc[0]["Product Name"]
lowest_margin = low_margin.iloc[0]["Gross Margin %"]

st.success(f"""
🏆 Highest Cost Product: **{highest_cost_product}**

💰 Product Cost: **${highest_cost:,.2f}**

📉 Lowest Margin Product: **{lowest_margin_product}**

📈 Margin: **{lowest_margin:.2f}%**

✅ Products with high cost and low margin should be reviewed to improve profitability.
""")

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.markdown("---")

st.subheader("📌 Strategic Recommendations")

st.info("""
✅ Reduce procurement cost for expensive products.

✅ Improve pricing strategy for low-margin products.

✅ Increase promotion of high-margin products.

✅ Monitor cost trends regularly using dashboard filters.

✅ Focus on improving profitability across divisions.
""")