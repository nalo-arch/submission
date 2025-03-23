import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np

st.set_page_config(page_title="Dashboard Analisis Data Bike Sharing", layout="wide")
sns.set(style="whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/main_data.csv', engine='python', encoding='utf-8')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

st.sidebar.header("Filter Data")
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()
start_date = st.sidebar.date_input("Mulai Tanggal", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Sampai Tanggal", max_date, min_value=min_date, max_value=max_date)
if start_date > end_date:
    st.sidebar.error("Mulai Tanggal harus sebelum atau sama dengan Sampai Tanggal.")
mask_date = (df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)
df_filtered = df.loc[mask_date]

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
available_seasons = sorted(df['season'].unique())
season_names = [season_mapping[s] for s in available_seasons]
selected_seasons = st.sidebar.multiselect("Pilih Musim", options=season_names, default=season_names)
selected_season_nums = [num for num, name in season_mapping.items() if name in selected_seasons]

available_weathers = sorted(df['weathersit_desc'].unique())
selected_weathers = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=available_weathers, default=available_weathers)

df_filtered = df_filtered[df_filtered['season'].isin(selected_season_nums) & df_filtered['weathersit_desc'].isin(selected_weathers)]
st.sidebar.write(f"Data tersisa: {df_filtered.shape[0]} baris")

st.title("Dashboard Analisis Data Bike Sharing")
st.markdown("""
Dashboard ini menyajikan hasil analisis data untuk menjawab dua pertanyaan bisnis utama:
1. **Distribusi Penyewaan Sepeda Berdasarkan Hari (Hari Kerja vs. Akhir Pekan)**
2. **Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda**
""")

st.header("Pertanyaan 1: Distribusi Berdasarkan Hari")
if 'weekday_name' not in df_filtered.columns:
    weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    df_filtered['weekday_name'] = df_filtered['weekday'].map(weekday_mapping)

avg_per_day = df_filtered.groupby('weekday_name')['cnt'].mean().reindex(['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
fig1, ax1 = plt.subplots(figsize=(8,4))
sns.barplot(x=avg_per_day.index, y=avg_per_day.values, palette='viridis', ax=ax1)
ax1.set_title("Rata-rata Penyewaan per Hari")
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(8,4))
sns.boxplot(x='weekday_name', y='cnt', data=df_filtered, order=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], palette='pastel', ax=ax2)
ax2.set_title("Distribusi Penyewaan Berdasarkan Hari")
st.pyplot(fig2)

df_hour['day_type'] = df_hour['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')

hourly_trend = df_hour.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=hourly_trend, x='hr', y='cnt', hue='day_type', marker='o', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Jam (Hari Kerja vs. Akhir Pekan)')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_xticks(range(0, 24))
ax.legend(title='Tipe Hari')

st.pyplot(fig)

st.header("Pertanyaan 2: Pengaruh Kondisi Cuaca terhadap Penyewaan")
weather_order = ['Clear', 'Mist', 'Light Rain', 'Heavy Rain']
fig4, ax4 = plt.subplots(figsize=(8,4))
sns.boxplot(x='weathersit_desc', y='cnt', data=df_filtered, order=weather_order, palette='coolwarm', ax=ax4)
ax4.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan")
st.pyplot(fig4)
