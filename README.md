🦠 COVID-19 vs Nipah Virus Comparative Dashboard

An interactive Streamlit-based data analytics dashboard that compares the spread, impact, and fatality of COVID-19 and Nipah Virus using real-world datasets.
This project combines Python, SQL, and data visualization to deliver meaningful public-health insights.

🚀 Live Demo

👉 (Add your Streamlit Cloud URL after deployment)

https://covid-nipah-dashboard-hu2tum4cahchxbjvdzyqke.streamlit.app/

📊 Dashboard Features
📌 Key Performance Indicators (KPIs)

COVID-19 Total Cases (auto formatted in K / M)

COVID-19 Total Deaths (auto formatted in K / M)

COVID-19 Fatality Rate (%)

Average Nipah Virus Fatality Rate (%)

🔍 Interactive Filters

Year-wise COVID-19 analysis

Country-wise Nipah outbreak filtering

📈 Visual Analytics

Line chart – COVID-19 fatality rate trend

Bar charts – COVID vs Nipah case comparison

Pie chart – COVID-19 case distribution

Heatmap – Nipah outbreaks by country & year

World map – COVID-19 global spread

Location map – Nipah outbreak regions

📄 Data Tables

Nipah outbreak dataset

Latest country-wise COVID-19 statistics

🛠️ Tech Stack

Python

Streamlit

Pandas

Matplotlib

Seaborn

Plotly

MySQL (for data storage & SQL analysis)

Jupyter Notebook

📂 Project Structure
covid-nipah-dashboard/
│
├── app1.py                           # Streamlit dashboard
├── COVID vs NIPAH.ipynb              # Jupyter Notebook analysis
├── covid_nipah_analysis_sql_code.sql # SQL queries for comparison
├── nipah_historical_outbreaks_updated.csv
├── owid-covid-data.zip
├── requirements.txt
├── README.md
└── covid vs nipah sample dashboard.pdf

📁 Datasets Used
🦠 COVID-19 Dataset

Source: Our World in Data (OWID)

Contains global case counts, deaths, testing, vaccination, and demographic indicators

🦠 Nipah Virus Dataset

Historical outbreak data

Country, year, cases, deaths, and CFR

▶️ How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/Shravani2712/your-repo-name.git
cd your-repo-name

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the Streamlit app
streamlit run app1.py

4️⃣ Upload datasets via sidebar (if required)
🌐 Deployment

Deployed using Streamlit Community Cloud

Connected directly to GitHub repository

Supports automatic redeployment on code updates

📌 SQL Integration

Database: covid_nipah_analysis

Tables:

covid_data

nipah_data

SQL queries used for:

Total case comparison

Fatality rate comparison

Year-wise and country-wise analysis

🎯 Use Cases

Academic mini / major projects

Data analytics portfolio

Public health data comparison

Streamlit dashboard demonstrations

👩‍💻 Author

Shravani Dhuri
Aspiring Data Analyst
Skills: Python | SQL | Excel | Tableau | Power BI | Streamlit
