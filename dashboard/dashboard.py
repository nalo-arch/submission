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

tabs = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Analisis Lanjutan"])

with tabs[0]:
    st.header("Pertanyaan 1: Distribusi Berdasarkan Hari")
    if 'weekday_name' not in df_filtered.columns:
        weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
        df_filtered['weekday_name'] = df_filtered['weekday'].map(weekday_mapping)
    
    avg_per_day = df_filtered.groupby('weekday_name')['cnt'].mean().reindex(['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    fig1, ax1 = plt.subplots(figsize=(8,4))
    sns.barplot(x=avg_per_day.index, y=avg_per_day.values, palette='viridis', ax=ax1)
    ax1.set_title("Rata-rata Penyewaan per Hari")
    ax1.set_xlabel("Hari")
    ax1.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig1)
    
    fig2, ax2 = plt.subplots(figsize=(8,4))
    sns.boxplot(x='weekday_name', y='cnt', data=df_filtered, order=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], palette='pastel', ax=ax2)
    ax2.set_title("Distribusi Penyewaan Berdasarkan Hari")
    st.pyplot(fig2)
    
    if 'hr_list' in df.columns and df['hr_list'].notna().any() and 'workingday_hour' in df.columns:
        all_hours = []
        day_types = []
        for idx, row in df.dropna(subset=['hr_list']).iterrows():
            dt = 'Weekday' if row['workingday_hour'] == 1 else 'Weekend'
            hr_list = row['hr_list']
            if isinstance(hr_list, str):
                hr_list = ast.literal_eval(hr_list)
            for h in hr_list:
                all_hours.append(h)
                day_types.append(dt)
        if all_hours:
            df_hour_agg = pd.DataFrame({'hr': all_hours, 'day_type': day_types})
            hourly_trend = df_hour_agg.groupby(['hr', 'day_type']).size().reset_index(name='count')
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=hourly_trend, x='hr', y='count', hue='day_type', marker='o', ax=ax3)
            ax3.set_title('Penyewaan Sepeda per Jam (Hari Kerja vs. Akhir Pekan)')
            ax3.set_xlabel('Jam')
            ax3.set_ylabel('Jumlah Penyewaan')
            ax3.set_xticks(range(0, 24))
            ax3.legend(title='Tipe Hari')
            st.pyplot(fig3)
        else:
            st.info("Tidak ada data jam yang tersedia.")
    else:
        st.info("Kolom 'hr_list' atau 'workingday_hour' tidak tersedia dalam file main_data.csv.")

with tabs[1]:
    st.header("Pertanyaan 2: Pengaruh Kondisi Cuaca terhadap Penyewaan")
    weather_order = ['Clear', 'Mist', 'Light Rain', 'Heavy Rain']
    fig4, ax4 = plt.subplots(figsize=(8,4))
    sns.boxplot(x='weathersit_desc', y='cnt', data=df_filtered, order=weather_order, palette='coolwarm', ax=ax4)
    ax4.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan")
    ax4.set_xlabel("Kondisi Cuaca")
    ax4.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig4)

with tabs[2]:
    st.header("Analisis Lanjutan")
    st.markdown("Analisis lanjutan mencakup tiga aspek:")
    
    st.subheader("1. Rata-rata Penyewaan Berdasarkan Suhu")
    temp_bins = [0, 0.3, 0.7, 1]
    temp_labels = ['Rendah', 'Sedang', 'Tinggi']
    df['temp_category'] = pd.cut(df['temp'], bins=temp_bins, labels=temp_labels, include_lowest=True)
    temp_analysis = df.groupby('temp_category')['cnt'].mean().reset_index()
    fig_temp, ax_temp = plt.subplots(figsize=(8,6))
    sns.barplot(x='temp_category', y='cnt', data=temp_analysis, palette='viridis', ax=ax_temp)
    ax_temp.set_title('Rata-rata Penyewaan Berdasarkan Kategori Suhu')
    ax_temp.set_xlabel('Kategori Suhu')
    ax_temp.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig_temp)
    
    st.subheader("2. Rata-rata Penyewaan Berdasarkan Kelembapan")
    hum_bins = [0, 0.4, 0.7, 1]
    hum_labels = ['Rendah', 'Sedang', 'Tinggi']
    df['hum_category'] = pd.cut(df['hum'], bins=hum_bins, labels=hum_labels, include_lowest=True)
    hum_analysis = df.groupby('hum_category')['cnt'].mean().reset_index()
    fig_hum, ax_hum = plt.subplots(figsize=(8,6))
    sns.barplot(x='hum_category', y='cnt', data=hum_analysis, palette='magma', ax=ax_hum)
    ax_hum.set_title('Rata-rata Penyewaan Berdasarkan Kategori Kelembapan')
    ax_hum.set_xlabel('Kategori Kelembapan')
    ax_hum.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig_hum)
    
    st.subheader("3. Rata-rata Penyewaan Berdasarkan Slot Waktu")
    if 'cnt_hour' in df.columns:
        def time_slot(hour):
            if 0 <= hour <= 5:
                return 'Early Morning'
            elif 6 <= hour <= 11:
                return 'Morning'
            elif 12 <= hour <= 17:
                return 'Afternoon'
            else:
                return 'Evening'
        df['time_slot'] = df['cnt_hour'].apply(time_slot)
        time_slot_analysis = df.groupby('time_slot')['cnt'].mean().reset_index()
        order = ['Early Morning','Morning','Afternoon','Evening']
        fig_slot, ax_slot = plt.subplots(figsize=(8,6))
        sns.barplot(x='time_slot', y='cnt', data=time_slot_analysis, order=order, palette='coolwarm', ax=ax_slot)
        ax_slot.set_title('Rata-rata Penyewaan Berdasarkan Slot Waktu')
        ax_slot.set_xlabel('Slot Waktu')
        ax_slot.set_ylabel('Rata-rata Penyewaan')
        st.pyplot(fig_slot)
    else:
        st.info("Data slot waktu tidak tersedia karena kolom 'cnt_hour' tidak ditemukan.")
