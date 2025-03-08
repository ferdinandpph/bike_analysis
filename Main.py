import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt_x": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "cnt_x": "order_count"
    }, inplace=True)

    return daily_orders_df


all_df = pd.read_csv("all_data.csv")

all_df["dteday"] = pd.to_datetime(all_df["dteday"], format="%Y-%m-%d")

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    
    st.header("Dashboard Sewa Sepeda")
    # Menambahkan logo 
    st.image("https://s3-alpha.figma.com/hub/file/1669985118/19ff14d3-805d-4254-b8ea-1da537a697a5-cover.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
        
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                 (all_df["dteday"] <= str(end_date))]

st.header('Penyewaan Sepeda :bike:')


# Section Nomor 1
st.subheader("1. Hubungan antara Kondisi Cuaca dan Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 6))

sns.set_palette("viridis")

all_weather = all_df.groupby('weathersit_x')['cnt_x'].mean().reset_index()

sns.barplot(x=all_weather['weathersit_x'],
            y=all_weather['cnt_x'], palette="mako", ax=ax)

ax.set_title("Hubungan antara Kondisi Cuaca dan Jumlah Penyewaan Sepeda")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan Sepeda (Rata-Rata)")

weather_conditions = ['Clear', 'Mist + Cloudy',
                      'Light Snow/Rain', 'Heavy Rain/Snow']
ax.set_xticks(ticks=range(4))
ax.set_xticklabels(weather_conditions)

plt.tight_layout()
st.pyplot(fig)  

# Section Nomor 2
st.subheader("2. Perbandingan Penyewaan Sepeda antara Hari Kerja dan Hari Libur")
fig, ax = plt.subplots(figsize=(12, 6))

sns.set_palette("Dark2")

all_days = all_df.groupby(['dteday', 'workingday_x'])[
    'cnt_x'].mean().reset_index()
work_day = all_days[all_days['workingday_x'] == 1]
holliday = all_days[all_days['workingday_x'] == 0]

sns.barplot(x=work_day['dteday'].dt.month, y=work_day['cnt_x'],
            color='darkcyan', alpha=0.7, label='Hari Kerja', ax=ax)

sns.barplot(x=holliday['dteday'].dt.month, y=holliday['cnt_x'],
            color='darkgreen', alpha=0.7, label='Hari Libur', ax=ax)

ax.set_title(
    'Perbandingan Penyewaan Sepeda antara Hari Kerja dan Hari Libur dalam Setahun')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan Sepeda (Rata-rata)')
ax.legend()

month = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
         "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
ax.set_xticks(ticks=range(12))
ax.set_xticklabels(month)

plt.tight_layout()
st.pyplot(fig)  

# Section Nomor 3
st.subheader("3. Perbandingan Penyewaan Sepeda antara Pengguna Casual dan Registered")
fig, ax = plt.subplots(figsize=(12, 6))

sns.set_palette("colorblind")

days_hour = all_df.groupby('hr').mean().reset_index()

sns.lineplot(x='hr', y='casual_x', data=days_hour, label='Casual Users', ax=ax)
sns.lineplot(x='hr', y='registered_x', data=days_hour,
             label='Registered Users', ax=ax)

ax.set_title(
    'Perbandingan Penyewaan Sepeda antara Pengguna Casual dan Terdaftar')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Jumlah Rata-rata Penyewaan Sepeda')

ax.legend()

plt.tight_layout()
st.pyplot(fig) 

