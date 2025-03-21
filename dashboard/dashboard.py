
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'main_data.csv')

df_day_cleaned = pd.read_csv(csv_path, engine='python', encoding='utf-8')
df_day_cleaned['dteday'] = pd.to_datetime(df_day_cleaned['dteday'])

st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Mulai Tanggal", df_day_cleaned['dteday'].min())
end_date = st.sidebar.date_input("Sampai Tanggal", df_day_cleaned['dteday'].max())
if start_date > end_date:
    st.sidebar.error("Mulai Tanggal harus lebih kecil atau sama dengan Sampai Tanggal.")

mask = (df_day_cleaned['dteday'] >= pd.to_datetime(start_date)) & (df_day_cleaned['dteday'] <= pd.to_datetime(end_date))
filtered_df = df_day_cleaned.loc[mask]

weather_options = st.sidebar.multiselect("Pilih Kondisi Cuaca",
                                           options=filtered_df['weathersit_desc'].unique(),
                                           default=filtered_df['weathersit_desc'].unique())
filtered_df = filtered_df[filtered_df['weathersit_desc'].isin(weather_options)]

st.write("Jumlah baris data setelah filter:", filtered_df.shape[0])

st.header("Dashboard Analisis Bike Sharing")

st.subheader("1. Rata-rata Penyewaan per Hari (Weekday vs. Weekend)")
weekday_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
df_avg = filtered_df.groupby('weekday_name')['cnt'].mean().reindex(weekday_order)
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(x=df_avg.index, y=df_avg.values, ax=ax1, palette='viridis')
ax1.set_title("Rata-rata Penyewaan per Hari")
ax1.set_xlabel("Hari")
ax1.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig1)

st.subheader("2. Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
weather_order = ['Clear', 'Mist', 'Light Rain', 'Heavy Rain']
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.boxplot(x='weathersit_desc', y='cnt', data=filtered_df, order=weather_order, ax=ax2, palette='coolwarm')
ax2.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig2)
