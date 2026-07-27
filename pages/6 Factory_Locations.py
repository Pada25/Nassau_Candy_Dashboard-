import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Factory Locations",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Factory Locations")

st.markdown("""
### Explore Nassau Candy manufacturing locations and the products produced at each factory.
""")

st.markdown("---")

# =====================================================
# FACTORY DATA
# =====================================================

factory_df = pd.DataFrame({

    "Factory":[
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Sugar Shack",
        "Secret Factory",
        "The Other Factory"
    ],

    "Latitude":[
        32.881893,
        32.076176,
        48.119140,
        41.446333,
        35.117500
    ],

    "Longitude":[
        -111.768036,
        -81.088371,
        -96.181150,
        -90.565487,
        -89.971107
    ],

    "Products":[
        "Nutty Crunch Surprise, Fudge Mallows, Scrumdiddlyumptious",
        "Milk Chocolate, Triple Dazzle Caramel",
        "Laffy Taffy, SweeTARTS, Nerds, Fun Dip, Fizzy Lifting Drinks",
        "Everlasting Gobstopper, Lickable Wallpaper, Wonka Gum",
        "Hair Toffee, Kazookles"
    ]
})

# =====================================================
# KPI
# =====================================================

c1,c2 = st.columns(2)

with c1:
    st.metric("🏭 Factories", len(factory_df))

with c2:
    st.metric("📦 Products", 15)

st.markdown("---")

# =====================================================
# MAP
# =====================================================

m = folium.Map(
    location=[39,-95],
    zoom_start=4
)

for _, row in factory_df.iterrows():

    folium.Marker(

        location=[row["Latitude"], row["Longitude"]],

        popup=f"""
        <b>{row['Factory']}</b><br><br>
        <b>Products:</b><br>{row['Products']}
        """,

        tooltip=row["Factory"],

        icon=folium.Icon(color="red", icon="industry", prefix="fa")

    ).add_to(m)

st.subheader("🗺️ Factory Locations")

st_folium(
    m,
    width=1200,
    height=600
)

# =====================================================
# FACTORY TABLE
# =====================================================

st.markdown("---")

st.subheader("📋 Factory Details")

st.dataframe(
    factory_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.markdown("---")

st.subheader("💡 Business Insights")

st.success("""
🏭 Nassau Candy products are manufactured across **5 production facilities**.

🍫 Chocolate products are concentrated in dedicated chocolate factories.

🍭 Sugar products are primarily manufactured at Sugar Shack.

📍 Mapping factories helps visualize production distribution and supports logistics planning.

🚚 Geographic analysis can assist in optimizing transportation and supply chain decisions.
""")