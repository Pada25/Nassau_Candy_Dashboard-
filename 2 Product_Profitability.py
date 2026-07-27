import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Product Profitability",
    page_icon="💰",
    layout="wide"
)

# =====================================================
# PAGE TITLE
# =====================================================
st.title("💰 Product Profitability Intelligence")

st.markdown("""
### Analyze product performance, profitability and margin contribution.

Use the interactive filters to identify the products driving business growth.
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
    "🏢 Division",
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
    st.warning("No products found for selected filters.")
    st.stop()

# =====================================================
# PRODUCT SUMMARY
# =====================================================

product_summary = (
    filtered_df
    .groupby("Product Name", as_index=False)
    .agg(
        {
            "Sales":"sum",
            "Cost":"sum",
            "Gross Profit":"sum",
            "Gross Margin %":"mean",
            "Profit Per Unit":"mean",
            "Profit Contribution %":"sum"
        }
    )
)

product_summary = product_summary.sort_values(
    by="Gross Profit",
    ascending=False
)

top_product = product_summary.iloc[0]["Product Name"]

highest_profit = product_summary.iloc[0]["Gross Profit"]

highest_margin = product_summary["Gross Margin %"].max()

total_products = product_summary["Product Name"].nunique()

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("🏆 Product Performance Highlights")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "🏆 Top Product",
        top_product
    )

with c2:
    st.metric(
        "💰 Highest Profit",
        f"${highest_profit:,.2f}"
    )

with c3:
    st.metric(
        "📈 Best Margin",
        f"{highest_margin:.2f}%"
    )

with c4:
    st.metric(
        "📦 Products",
        total_products
    )

st.markdown("---")

# =====================================================
# TOP PRODUCTS
# =====================================================

top_products = product_summary.head(10)

left,right = st.columns(2)

with left:

    fig = px.bar(
        top_products,
        x="Product Name",
        y="Gross Profit",
        color="Gross Margin %",
        text="Gross Profit",
        color_continuous_scale="Viridis",
        title="🏆 Top 10 Products by Gross Profit"
    )

    fig.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        height=520,
        xaxis_tickangle=-35
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    pie = px.pie(
        top_products,
        names="Product Name",
        values="Gross Profit",
        hole=0.45,
        title="🥧 Profit Contribution"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )
    # =====================================================
# PRODUCT PERFORMANCE LEADERBOARD
# =====================================================

st.markdown("---")

st.subheader("🏅 Product Performance Leaderboard")

leaderboard = top_products.copy()

leaderboard["Sales"] = leaderboard["Sales"].round(2)
leaderboard["Cost"] = leaderboard["Cost"].round(2)
leaderboard["Gross Profit"] = leaderboard["Gross Profit"].round(2)
leaderboard["Gross Margin %"] = leaderboard["Gross Margin %"].round(2)
leaderboard["Profit Per Unit"] = leaderboard["Profit Per Unit"].round(2)
leaderboard["Profit Contribution %"] = leaderboard["Profit Contribution %"].round(2)

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# TOP 5 MOST PROFITABLE PRODUCTS
# =====================================================

st.markdown("---")

st.subheader("⭐ Top 5 Most Profitable Products")

top5 = leaderboard.head(5)

st.table(
    top5[
        [
            "Product Name",
            "Gross Profit",
            "Gross Margin %",
            "Profit Contribution %"
        ]
    ]
)

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.markdown("---")

st.subheader("💡 Business Insights")

highest_margin_product = leaderboard.loc[
    leaderboard["Gross Margin %"].idxmax(),
    "Product Name"
]

highest_margin_value = leaderboard["Gross Margin %"].max()

highest_contribution_product = leaderboard.loc[
    leaderboard["Profit Contribution %"].idxmax(),
    "Product Name"
]

highest_contribution = leaderboard["Profit Contribution %"].max()

st.success(f"""
🏆 **Top Revenue Generating Product:** **{top_product}**

💰 **Highest Total Gross Profit:** **${highest_profit:,.2f}**

📈 **Highest Margin Product:** **{highest_margin_product}** ({highest_margin_value:.2f}%)

🥧 **Largest Profit Contributor:** **{highest_contribution_product}**
({highest_contribution:.2f}%)

📦 **Products Analysed:** **{total_products}**
""")

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.markdown("---")

st.subheader("📌 Strategic Recommendations")

st.info("""
✅ Focus inventory planning on high-profit products.

✅ Promote products with high gross margins through targeted marketing.

✅ Review products with low contribution and optimize pricing or sourcing.

✅ Use dashboard filters to compare products across different divisions and time periods.
""")