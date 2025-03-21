import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Analisis Bike Sharing", layout="wide")
sns.set(style="whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/main_data.csv', engine='python', encoding='utf-8')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

st.sidebar.header("Filter Data")
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
available_seasons = sorted(df['season'].unique())
season_names = [season_mapping[s] for s in available_seasons]
selected_seasons = st.sidebar.multiselect("Pilih Musim", options=season_names, default=season_names)
selected_season_nums = [num for num, name in season_mapping.items() if name in selected_seasons]

available_weathers = sorted(df['weathersit_desc'].unique())
selected_weathers = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=available_weathers, default=available_weathers)

df_filtered = df[df['season'].isin(selected_season_nums) & df['weathersit_desc'].isin(selected_weathers)]

st.sidebar.write(f"Data tersisa: {df_filtered.shape[0]} baris")

st.title("Dashboard Analisis Data Bike Sharing")
st.markdown("""
Dashboard ini menyajikan hasil analisis data untuk menjawab dua pertanyaan bisnis utama:
1. **Distribusi Penyewaan Sepeda Berdasarkan Hari (Hari Kerja vs. Akhir Pekan)**
2. **Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda**
""")

st.header("Pertanyaan 1: Distribusi Penyewaan Berdasarkan Hari")

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
ax2.set_xlabel("Hari")
ax2.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig2)

if 'hr' in df_filtered.columns and 'workingday' in df_filtered.columns:
    df_filtered['day_type'] = df_filtered['workingday'].apply(lambda x: 'Weekday' if x==1 else 'Weekend')
    line_data = df_filtered.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(8,4))
    sns.lineplot(data=line_data, x='hr', y='cnt', hue='day_type', marker='o', ax=ax3)
    ax3.set_title("Rata-rata Penyewaan per Jam (Weekday vs. Weekend)")
    ax3.set_xlabel("Jam")
    ax3.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig3)
else:
    st.info("Data jam atau informasi workingday tidak tersedia untuk analisis per jam.")

st.header("Pertanyaan 2: Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

weather_order = ['Clear', 'Mist', 'Light Rain', 'Heavy Rain']
fig4, ax4 = plt.subplots(figsize=(8,4))
sns.boxplot(x='weathersit_desc', y='cnt', data=df_filtered, order=weather_order, palette='coolwarm', ax=ax4)
ax4.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan")
ax4.set_xlabel("Kondisi Cuaca")
ax4.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig4)

st.header("Analisis Lanjutan")

if 'temp' in df_filtered.columns:
    fig5, ax5 = plt.subplots(figsize=(8,4))
    sns.scatterplot(x='temp', y='cnt', data=df_filtered, color='teal', ax=ax5)
    ax5.set_title("Hubungan Suhu dan Penyewaan")
    ax5.set_xlabel("Suhu (Normalisasi)")
    ax5.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig5)
else:
    st.info("Kolom 'temp' tidak tersedia.")

if 'temp' in df_filtered.columns:
    temp_bins = [0, 0.3, 0.7, 1]
    temp_labels = ['Rendah', 'Sedang', 'Tinggi']
    df_filtered['temp_category'] = pd.cut(df_filtered['temp'], bins=temp_bins, labels=temp_labels, include_lowest=True)
    temp_avg = df_filtered.groupby('temp_category')['cnt'].mean().reset_index()
    fig6, ax6 = plt.subplots(figsize=(8,4))
    sns.barplot(x='temp_category', y='cnt', data=temp_avg, palette='magma', ax=ax6)
    ax6.set_title("Penyewaan Berdasarkan Kategori Suhu")
    ax6.set_xlabel("Kategori Suhu")
    ax6.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig6)

if 'hum' in df_filtered.columns:
    hum_bins = [0, 0.4, 0.7, 1]
    hum_labels = ['Rendah', 'Sedang', 'Tinggi']
    df_filtered['hum_category'] = pd.cut(df_filtered['hum'], bins=hum_bins, labels=hum_labels, include_lowest=True)
    hum_avg = df_filtered.groupby('hum_category')['cnt'].mean().reset_index()
    fig7, ax7 = plt.subplots(figsize=(8,4))
    sns.barplot(x='hum_category', y='cnt', data=hum_avg, palette='coolwarm', ax=ax7)
    ax7.set_title("Penyewaan Berdasarkan Kategori Kelembapan")
    ax7.set_xlabel("Kategori Kelembapan")
    ax7.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig7)

if 'hr' in df_filtered.columns:
    def time_slot(hr):
        if 0 <= hr < 6:
            return 'Early Morning'
        elif 6 <= hr < 12:
            return 'Morning'
        elif 12 <= hr < 18:
            return 'Afternoon'
        else:
            return 'Evening'
    df_filtered['time_slot'] = df_filtered['hr'].apply(time_slot)
    slot_avg = df_filtered.groupby('time_slot')['cnt'].mean().reindex(['Early Morning', 'Morning', 'Afternoon', 'Evening'])
    fig8, ax8 = plt.subplots(figsize=(8,4))
    sns.barplot(x=slot_avg.index, y=slot_avg.values, palette='Set2', ax=ax8)
    ax8.set_title("Penyewaan Berdasarkan Slot Waktu")
    ax8.set_xlabel("Slot Waktu")
    ax8.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig8)
else:
    st.info("Data jam tidak tersedia untuk analisis slot waktu.")

st.header("Heatmap Korelasi antar Fitur (Dataset Day)")
corr = df_filtered.corr()
fig9, ax9 = plt.subplots(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax9)
ax9.set_title("Heatmap Korelasi antar Fitur")
st.pyplot(fig9)
