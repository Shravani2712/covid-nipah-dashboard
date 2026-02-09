import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="COVID-19 vs Nipah Virus Dashboard",
    layout="wide"
)

st.title("🦠 COVID-19 vs Nipah Virus Comparative Analysis")
st.markdown(
    "This dashboard compares the spread, impact, and fatality of **COVID-19** and **Nipah Virus** using real-world datasets."
)

# ------------------ HELPER FUNCTION ------------------
def format_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(int(num))

# ------------------ FILE UPLOAD ------------------
st.sidebar.header("📂 Upload Datasets")

covid_file = st.sidebar.file_uploader(
    "Upload OWID COVID Dataset (CSV)",
    type=["csv"]
)

nipah_file = st.sidebar.file_uploader(
    "Upload Nipah Dataset (CSV)",
    type=["csv"]
)

if covid_file is None or nipah_file is None:
    st.warning("⬅️ Please upload BOTH COVID and Nipah CSV files to continue.")
    st.stop()

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data(covid_file, nipah_file):
    covid = pd.read_csv(covid_file)
    nipah = pd.read_csv(nipah_file)
    return covid, nipah

covid, nipah = load_data(covid_file, nipah_file)

# ------------------ COVID DATA PROCESSING ------------------
covid = covid[['iso_code', 'location', 'date', 'total_cases', 'total_deaths', 'population']]
covid = covid.dropna(subset=['iso_code', 'total_cases'])

covid['date'] = pd.to_datetime(covid['date'])
covid['year'] = covid['date'].dt.year

covid_yearly = covid.groupby('year').agg(
    total_cases=('total_cases', 'max'),
    total_deaths=('total_deaths', 'max')
).reset_index()

covid_yearly['fatality_rate'] = (
    covid_yearly['total_deaths'] / covid_yearly['total_cases']
) * 100

covid_latest = covid.sort_values('date').drop_duplicates(
    subset=['location'], keep='last'
)

# ------------------ NIPAH DATA PROCESSING ------------------
nipah = nipah[['Year', 'Country', 'Cases', 'Deaths']]
nipah['fatality_rate'] = (nipah['Deaths'] / nipah['Cases']) * 100

nipah_coords = {
    "India": [20.5937, 78.9629],
    "Bangladesh": [23.6850, 90.3563],
    "Malaysia": [4.2105, 101.9758],
    "Singapore": [1.3521, 103.8198]
}

nipah['latitude'] = nipah['Country'].map(lambda x: nipah_coords.get(x, [None, None])[0])
nipah['longitude'] = nipah['Country'].map(lambda x: nipah_coords.get(x, [None, None])[1])
nipah_map = nipah.dropna(subset=['latitude', 'longitude'])

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("🔍 Filters")

selected_year = st.sidebar.slider(
    "Select COVID Year",
    int(covid_yearly['year'].min()),
    int(covid_yearly['year'].max()),
    int(covid_yearly['year'].max())
)

selected_country = st.sidebar.selectbox(
    "Select Nipah Country",
    ["All"] + sorted(nipah['Country'].unique())
)

nipah_filtered = nipah if selected_country == "All" else nipah[nipah['Country'] == selected_country]

# ------------------ KPI SECTION ------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

covid_selected = covid_yearly[covid_yearly['year'] == selected_year]

col1.metric(
    "COVID Total Cases",
    format_number(float(covid_selected['total_cases']))
)

col2.metric(
    "COVID Total Deaths",
    format_number(float(covid_selected['total_deaths']))
)

col3.metric(
    "COVID Fatality Rate (%)",
    round(float(covid_selected['fatality_rate']), 2)
)

col4.metric(
    "Avg Nipah Fatality Rate (%)",
    round(nipah_filtered['fatality_rate'].mean(), 2)
)

# ------------------ LINE CHART ------------------
st.subheader("📈 COVID-19 Fatality Rate Trend")

fig1, ax1 = plt.subplots()
ax1.plot(covid_yearly['year'], covid_yearly['fatality_rate'], marker='o')
ax1.set_xlabel("Year")
ax1.set_ylabel("Fatality Rate (%)")
st.pyplot(fig1)

# ------------------ BAR CHARTS ------------------
st.subheader("📊 Case Comparison")

col5, col6 = st.columns(2)

with col5:
    fig2, ax2 = plt.subplots()
    ax2.bar(covid_yearly['year'], covid_yearly['total_cases'] / 1e6)
    ax2.set_title("COVID-19 Cases (Millions)")
    st.pyplot(fig2)

with col6:
    fig3, ax3 = plt.subplots()
    ax3.bar(nipah_filtered['Year'], nipah_filtered['Cases'])
    ax3.set_title("Nipah Virus Cases")
    st.pyplot(fig3)

# ------------------ PIE CHART ------------------
st.subheader("🥧 COVID-19 Case Distribution")

pie_values = [
    covid_selected['total_cases'].values[0] - covid_selected['total_deaths'].values[0],
    covid_selected['total_deaths'].values[0]
]

fig4, ax4 = plt.subplots()
ax4.pie(
    pie_values,
    labels=["Recovered / Active", "Deaths"],
    autopct="%1.1f%%"
)
st.pyplot(fig4)

# ------------------ HEATMAP ------------------
st.subheader("🔥 Nipah Cases Heatmap")

heatmap_data = nipah.pivot_table(
    values="Cases",
    index="Country",
    columns="Year",
    fill_value=0
)

fig5, ax5 = plt.subplots(figsize=(10, 4))
sns.heatmap(heatmap_data, cmap="Reds", annot=True, fmt=".0f", ax=ax5)
st.pyplot(fig5)

# ------------------ MAPS ------------------
st.subheader("🌍 Geographical Spread")

col7, col8 = st.columns(2)

with col7:
    st.markdown("**COVID-19 Global Spread**")
    covid_map = px.choropleth(
        covid_latest,
        locations="iso_code",
        color="total_cases",
        hover_name="location",
        color_continuous_scale="Reds",
        title="COVID-19 Total Cases by Country"
    )
    st.plotly_chart(covid_map, use_container_width=True)

with col8:
    st.markdown("**Nipah Virus Outbreak Locations**")
    st.map(
        nipah_map.rename(columns={"latitude": "lat", "longitude": "lon"})[['lat', 'lon']]
    )

# ------------------ DATA TABLES ------------------
st.subheader("📄 Nipah Outbreak Dataset")
st.dataframe(nipah_filtered)

st.subheader("📄 COVID-19 Dataset (Latest Country-wise)")
st.dataframe(
    covid_latest[['location', 'total_cases', 'total_deaths', 'population']]
)