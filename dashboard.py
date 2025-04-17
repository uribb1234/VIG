import os
import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# התחברות עם ENV
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER", "avnadmin")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))

# יצירת Engine
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# קריאת נתונים
@st.cache_data
def load_data():
    query = "SELECT date, time, site FROM news_updates"
    df = pd.read_sql(query, engine)
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], errors='coerce')
    df.dropna(subset=["datetime"], inplace=True)
    return df

st.title("📊 דשבורד מבזקי חדשות")

df = load_data()

# גרף לפי שעה
st.subheader("כמות כותרות לפי שעה")
df["hour"] = df["datetime"].dt.hour
hourly_counts = df.groupby("hour").size()
st.bar_chart(hourly_counts)

# גרף לפי מקור
st.subheader("פילוח לפי מקורות")
site_counts = df["site"].value_counts()
st.bar_chart(site_counts)
