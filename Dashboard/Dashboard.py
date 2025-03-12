import pandas as pd
import plotly.express as px
import streamlit as st

# Load Data
df = pd.read_csv(r"C:\Users\ASUS\Downloads\Submission\Dashboard\all_data.csv")

# Data Preprocessing
df = df[["dteday", "season_x", "mnth_x", "hr", "casual_x", "registered_x", "cnt_x", "weathersit_x", "workingday_x"]]
df.rename(columns={
    "dteday": "date",
    "season_x": "season",
    "mnth_x": "month",
    "hr": "hour",
    "casual_x": "casual_users",
    "registered_x": "registered_users",
    "cnt_x": "total_rentals",
    "weathersit_x": "weather",
    "workingday_x": "is_workingday"
}, inplace=True)

df["date"] = pd.to_datetime(df["date"])

# Mapping Season Labels
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df["season"] = df["season"].map(season_labels)

# Sidebar
st.sidebar.image("https://img.freepik.com/free-vector/family-weekend-outdoors_74855-4788.jpg", use_container_width=True)
st.sidebar.title("🚲 Bike Sharing Dashboard")

start_date, end_date = st.sidebar.date_input("Rentang Waktu", [df["date"].min(), df["date"].max()])
df_filtered = df[(df["date"] >= pd.Timestamp(start_date)) & (df["date"] <= pd.Timestamp(end_date))]

# Main Dashboard
st.title("📊 Bike Share Analytics")
st.markdown("---")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", df_filtered["total_rentals"].sum())
col2.metric("Total Registered", df_filtered["registered_users"].sum())
col3.metric("Total Casual", df_filtered["casual_users"].sum())

# Grafik Penyewaan Berdasarkan Musim
st.subheader("📅 Penyewaan Sepeda Berdasarkan Musim")
fig_season = px.bar(df_filtered, x="season", y="total_rentals", color="season", title="Total Penyewaan per Musim", labels={"total_rentals": "Jumlah Penyewaan"})
st.plotly_chart(fig_season)

# Grafik Penyewaan Berdasarkan Jam
st.subheader("⏰ Jam Paling Ramai dan Sepi untuk Penyewaan")
hourly_count = df_filtered.groupby("hour")["total_rentals"].sum().reset_index()
fig_hour = px.line(hourly_count, x="hour", y="total_rentals", markers=True, title="Penyewaan Sepeda per Jam")
st.plotly_chart(fig_hour)

# Pie Chart Perbandingan AM vs PM
st.subheader("☀️🌙 Perbandingan Penyewaan AM vs PM")
df_filtered["time_period"] = pd.cut(df_filtered["hour"], bins=[0, 11, 23], labels=["AM", "PM"], right=False)
am_pm_count = df_filtered.groupby("time_period")["total_rentals"].sum().reset_index()
fig_pie = px.pie(am_pm_count, names="time_period", values="total_rentals", title="Penyewaan Sepeda AM vs PM")
st.plotly_chart(fig_pie)

# Penyewaan per Bulan
st.subheader("📈 Performa Penyewaan Sepeda per Bulan")
monthly_count = df_filtered.groupby("month")["total_rentals"].sum().reset_index()
fig_monthly = px.line(monthly_count, x="month", y="total_rentals", markers=True, title="Penyewaan Sepeda per Bulan")
st.plotly_chart(fig_monthly)

# Perbandingan Penyewaan Berdasarkan Kondisi Cuaca
st.subheader("🌦️ Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
weather_labels = {1: "Clear", 2: "Mist + Cloudy", 3: "Light Snow/Rain", 4: "Heavy Rain/Snow"}
df_filtered["weather"] = df_filtered["weather"].map(weather_labels)
weather_count = df_filtered.groupby("weather")["total_rentals"].mean().reset_index()
fig_weather = px.bar(weather_count, x="weather", y="total_rentals", color="weather", title="Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
st.plotly_chart(fig_weather)

# Perbandingan Penyewaan Sepeda antara Hari Kerja dan Hari Libur
st.subheader("🏢 vs 🎉 Penyewaan Sepeda: Hari Kerja vs Hari Libur")
workingday_count = df_filtered.groupby("is_workingday")["total_rentals"].mean().reset_index()
workingday_count["is_workingday"] = workingday_count["is_workingday"].map({1: "Hari Kerja", 0: "Hari Libur"})
fig_workingday = px.bar(workingday_count, x="is_workingday", y="total_rentals", color="is_workingday", title="Penyewaan Sepeda pada Hari Kerja dan Libur")
st.plotly_chart(fig_workingday)

# Perbandingan Penyewaan Sepeda antara Pengguna Casual dan Terdaftar
st.subheader("👥 Pengguna Casual vs Terdaftar")
casual_registered = df_filtered.groupby("hour")[["casual_users", "registered_users"]].mean().reset_index()
fig_users = px.line(casual_registered, x="hour", y=["casual_users", "registered_users"], markers=True, title="Penyewaan Sepeda: Casual vs Registered")
st.plotly_chart(fig_users)