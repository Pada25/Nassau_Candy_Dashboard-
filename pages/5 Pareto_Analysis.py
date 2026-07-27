import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Pareto Analysis",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📈 Pareto Analysis (80/20 Rule)")

st.markdown("""
### Identify the products contributing the most to total business profit.
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
# PRODUCT SUMMARY
# =====================================================

pareto = (
    filtered_df.groupby("Product Name", as_index=False)
    .agg({
        "Gross Profit":"sum",
        "Sales":"sum"
    })
)

pareto = pareto.sort_values(
    "Gross Profit",
    ascending=False
)

pareto["Cumulative Profit"] = pareto["Gross Profit"].cumsum()

pareto["Cumulative %"] = (
    pareto["Cumulative Profit"] /
    pareto["Gross Profit"].sum()
) * 100

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("📊 Pareto Summary")

c1,c2,c3 = st.columns(3)

with c1:
    st.metric("📦 Products", len(pareto))

with c2:
    st.metric(
        "💰 Total Profit",
        f"${pareto['Gross Profit'].sum():,.2f}"
    )

with c3:
    st.metric(
        "🏆 Top Product",
        pareto.iloc[0]["Product Name"]
    )

st.markdown("---")

# =====================================================
# BAR CHART
# =====================================================

bar = px.bar(
    pareto.head(10),
    x="Product Name",
    y="Gross Profit",
    color="Gross Profit",
    text="Gross Profit",
    color_continuous_scale="Viridis",
    title="🏆 Top 10 Products by Gross Profit"
)

bar.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

bar.update_layout(
    height=500,
    xaxis_tickangle=-30
)

st.plotly_chart(
    bar,
    use_container_width=True
)

# =====================================================
# CUMULATIVE PARETO LINE
# =====================================================

line = px.line(
    pareto,
    x="Product Name",
    y="Cumulative %",
    markers=True,
    title="📈 Cumulative Profit Percentage"
)

line.update_layout(
    height=500,
    xaxis_tickangle=-45,
    yaxis_title="Cumulative Profit (%)"
)

st.plotly_chart(
    line,
    use_container_width=True
)

# =====================================================
# PARETO TABLE
# =====================================================

st.markdown("---")

st.subheader("🏅 Pareto Leaderboard")

st.dataframe(
    pareto,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.markdown("---")

st.subheader("💡 Business Insights")

top_product = pareto.iloc[0]["Product Name"]

top_profit = pareto.iloc[0]["Gross Profit"]

st.success(f"""
🏆 Top Product: **{top_product}**

💰 Gross Profit: **${top_profit:,.2f}**

📈 A small number of products contribute to the majority of total business profit.

✅ Focus marketing and inventory planning on these high-performing products.
""")

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.markdown("---")

st.subheader("📌 Strategic Recommendations")

st.info("""
✅ Prioritize inventory for top-performing products.

✅ Focus marketing campaigns on products generating maximum profit.

✅ Monitor products with low contribution regularly.

✅ Apply the Pareto principle to maximize business growth.

✅ Use dashboard filters for detailed product-level analysis.
""")