import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Division Performance",
    page_icon="🏢",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🏢 Division Performance Intelligence")

st.markdown("""
### Analyze division-wise revenue, profitability and margin performance.

Compare business divisions to identify the strongest contributors to company profit.
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
    st.warning("No records found for selected filters.")
    st.stop()

# =====================================================
# DIVISION SUMMARY
# =====================================================

division_summary = (
    filtered_df
    .groupby("Division", as_index=False)
    .agg(
        {
            "Sales":"sum",
            "Cost":"sum",
            "Gross Profit":"sum",
            "Gross Margin %":"mean",
            "Profit Per Unit":"mean"
        }
    )
)

division_summary = division_summary.sort_values(
    "Gross Profit",
    ascending=False
)

best_division = division_summary.iloc[0]["Division"]

total_sales = division_summary["Sales"].sum()

total_profit = division_summary["Gross Profit"].sum()

average_margin = division_summary["Gross Margin %"].mean()

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("🏆 Division Performance Highlights")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "🥇 Best Division",
        best_division
    )

with c2:
    st.metric(
        "💰 Total Revenue",
        f"${total_sales:,.2f}"
    )

with c3:
    st.metric(
        "💵 Total Profit",
        f"${total_profit:,.2f}"
    )

with c4:
    st.metric(
        "📈 Average Margin",
        f"{average_margin:.2f}%"
    )

st.markdown("---")

# =====================================================
# CHARTS
# =====================================================

left,right = st.columns(2)

with left:

    revenue_chart = px.bar(
        division_summary,
        x="Division",
        y="Sales",
        color="Gross Profit",
        color_continuous_scale="Viridis",
        text="Sales",
        title="💰 Revenue by Division"
    )

    revenue_chart.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    revenue_chart.update_layout(height=500)

    st.plotly_chart(
        revenue_chart,
        use_container_width=True
    )

with right:

    profit_chart = px.pie(
        division_summary,
        names="Division",
        values="Gross Profit",
        hole=0.45,
        title="🥧 Profit Contribution by Division"
    )

    st.plotly_chart(
        profit_chart,
        use_container_width=True
    )
    # =====================================================
# MARGIN DISTRIBUTION
# =====================================================

st.markdown("---")

st.subheader("📈 Margin Distribution by Division")

margin_chart = px.bar(
    division_summary,
    x="Division",
    y="Gross Margin %",
    color="Gross Margin %",
    color_continuous_scale="RdYlGn",
    text="Gross Margin %",
    title="Average Gross Margin by Division"
)

margin_chart.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

margin_chart.update_layout(
    height=450,
    xaxis_title="Division",
    yaxis_title="Average Gross Margin (%)"
)

st.plotly_chart(
    margin_chart,
    use_container_width=True
)

# =====================================================
# DIVISION PERFORMANCE SCOREBOARD
# =====================================================

st.markdown("---")

st.subheader("🏆 Division Performance Scoreboard")

scoreboard = division_summary.copy()

scoreboard["Sales"] = scoreboard["Sales"].round(2)
scoreboard["Cost"] = scoreboard["Cost"].round(2)
scoreboard["Gross Profit"] = scoreboard["Gross Profit"].round(2)
scoreboard["Gross Margin %"] = scoreboard["Gross Margin %"].round(2)
scoreboard["Profit Per Unit"] = scoreboard["Profit Per Unit"].round(2)

scoreboard = scoreboard.rename(
    columns={
        "Sales":"Revenue",
        "Cost":"Cost",
        "Gross Profit":"Profit",
        "Gross Margin %":"Margin (%)",
        "Profit Per Unit":"Profit / Unit"
    }
)

st.dataframe(
    scoreboard,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.markdown("---")

st.subheader("💡 Executive Insights")

top_division = scoreboard.iloc[0]["Division"]
top_profit = scoreboard.iloc[0]["Profit"]
top_margin = scoreboard.iloc[0]["Margin (%)"]

lowest_margin = scoreboard.loc[
    scoreboard["Margin (%)"].idxmin(),
    "Division"
]

st.success(f"""
🏆 **Top Performing Division:** {top_division}

💰 **Highest Gross Profit:** ${top_profit:,.2f}

📈 **Average Gross Margin:** {top_margin:.2f}%

⚠️ **Lowest Margin Division:** {lowest_margin}

✅ Focus on expanding the strongest division while improving pricing and cost efficiency in lower-margin divisions.
""")

# =====================================================
# STRATEGIC RECOMMENDATIONS
# =====================================================

st.markdown("---")

st.subheader("📌 Strategic Recommendations")

st.info("""
✅ Invest more in high-performing divisions.

✅ Review pricing strategy for low-margin divisions.

✅ Optimize procurement and operational costs.

✅ Monitor division-wise profitability regularly using dashboard filters.

✅ Use this analysis to support business expansion and inventory planning.
""")