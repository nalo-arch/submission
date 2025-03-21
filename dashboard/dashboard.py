import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Atur tampilan Streamlit
st.set_page_config(page_title="Dashboard Analisis Bike Sharing", layout="wide")
sns.set(style="whitegrid")

# Baca file CSV yang sudah valid
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/main_data.csv', engine='python', encoding='utf-8')
    # Pastikan kolom tanggal dalam format datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Sidebar: Filter Interaktif
st.sidebar.header("Filter Data")
# Filter berdasarkan rentang tanggal
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()
start_date = st.sidebar.date_input("Mulai Tanggal", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Sampai Tanggal", max_date, min_value=min_date, max_value=max_date)
if start_date > end_date:
    st.sidebar.error("Mulai Tanggal harus sebelum atau sama dengan Sampai Tanggal.")
    
# Filter data berdasarkan tanggal
mask_date = (df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)
df_filtered = df.loc[mask_date]

# Filter berdasarkan kondisi cuaca (menggunakan mapping weathersit_desc)
weather_options = st.sidebar.multiselect("Pilih Kondisi Cuaca", 
                                           options=sorted(df['weathersit_desc'].unique()),
                                           default=sorted(df['weathersit_desc'].unique()))
df_filtered = df_filtered[df_filtered['weathersit_desc'].isin(weather_options)]

st.sidebar.write(f"Data yang tersisa: {df_filtered.shape[0]} baris")

st.title("Dashboard Analisis Data Bike Sharing")
st.write("Dashboard ini menyajikan analisis berdasarkan dua pertanyaan bisnis utama:")

st.markdown("**Pertanyaan 1:** Bagaimana distribusi penyewaan sepeda sepanjang hari (hari kerja vs. akhir pekan)?")
st.markdown("**Pertanyaan 2:** Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?")

# --- Bagian 1: Analisis Berdasarkan Hari ---
st.header("Pertanyaan 1: Analisis Berdasarkan Hari")

# Visualisasi 1.1: Trend Penyewaan Harian
fig_trend, ax_trend = plt.subplots(figsize=(10, 4))
# Plot garis jumlah penyewaan per tanggal
ax_trend.plot(df_filtered['dteday'], df_filtered['cnt'], marker='o', linestyle='-', color='b')
ax_trend.set_title("Trend Penyewaan Sepeda Harian")
ax_trend.set_xlabel("Tanggal")
ax_trend.set_ylabel("Jumlah Penyewaan")
plt.xticks(rotation=45)
st.pyplot(fig_trend)

# Visualisasi 1.2: Rata-rata Penyewaan per Hari dalam Seminggu
# Pastikan urutan hari konsisten
hari_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
avg_by_day = df_filtered.groupby('weekday_name')['cnt'].mean().reindex(hari_order)
fig_bar, ax_bar = plt.subplots(figsize=(8, 4))
sns.barplot(x=avg_by_day.index, y=avg_by_day.values, palette='viridis', ax=ax_bar)
ax_bar.set_title("Rata-rata Penyewaan per Hari")
ax_bar.set_xlabel("Hari")
ax_bar.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig_bar)

# Analisis Lanjutan (Hari): Misalnya, segmentasi waktu (jika ada kolom waktu dari dataset hour atau pembagian jam)
if 'hr' in df.columns:
    st.subheader("Analisis Lanjutan Berdasarkan Waktu (Dataset Hour)")
    # Filter data dari dataset df_hour (misalnya, menggunakan kolom 'hr')
    # Asumsikan df_hour juga sudah diolah serupa dan tersedia sebagai bagian dari df (atau bisa load terpisah)
    # Misal: Kelompokkan jam ke dalam slot waktu
    def time_slot(hr):
        if 0 <= hr < 6:
            return 'Early Morning'
        elif 6 <= hr < 12:
            return 'Morning'
        elif 12 <= hr < 18:
            return 'Afternoon'
        else:
            return 'Evening'
    if 'hr' in df_filtered.columns:
        df_filtered['time_slot'] = df_filtered['hr'].apply(time_slot)
        slot_avg = df_filtered.groupby('time_slot')['cnt'].mean().reindex(['Early Morning','Morning','Afternoon','Evening'])
        fig_slot, ax_slot = plt.subplots(figsize=(8, 4))
        sns.barplot(x=slot_avg.index, y=slot_avg.values, palette='coolwarm', ax=ax_slot)
        ax_slot.set_title("Rata-rata Penyewaan Berdasarkan Slot Waktu")
        ax_slot.set_xlabel("Slot Waktu")
        ax_slot.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig_slot)
    else:
        st.info("Kolom 'hr' tidak tersedia di dataset.")

# --- Bagian 2: Analisis Berdasarkan Cuaca ---
st.header("Pertanyaan 2: Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

# Visualisasi 2.1: Boxplot Penyewaan Berdasarkan Kondisi Cuaca
weather_order = ['Clear', 'Mist', 'Light Rain', 'Heavy Rain']
fig_box, ax_box = plt.subplots(figsize=(8, 4))
sns.boxplot(x='weathersit_desc', y='cnt', data=df_filtered, order=weather_order, palette='coolwarm', ax=ax_box)
ax_box.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
ax_box.set_xlabel("Kondisi Cuaca")
ax_box.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig_box)

# Visualisasi 2.2: Scatter Plot Suhu vs. Penyewaan
if 'temp' in df_filtered.columns:
    fig_scatter, ax_scatter = plt.subplots(figsize=(8, 4))
    sns.scatterplot(x='temp', y='cnt', data=df_filtered, ax=ax_scatter, color='teal')
    ax_scatter.set_title("Hubungan Suhu dengan Penyewaan Sepeda")
    ax_scatter.set_xlabel("Suhu (Normalisasi)")
    ax_scatter.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig_scatter)
else:
    st.info("Kolom 'temp' tidak tersedia di dataset.")

# Analisis Lanjutan (Cuaca): Misalnya, binning suhu untuk melihat kategori suhu
if 'temp' in df_filtered.columns:
    st.subheader("Analisis Lanjutan: Kategori Suhu")
    temp_bins = [0, 0.3, 0.7, 1]
    temp_labels = ['Rendah', 'Sedang', 'Tinggi']
    df_filtered['temp_category'] = pd.cut(df_filtered['temp'], bins=temp_bins, labels=temp_labels, include_lowest=True)
    temp_cat_avg = df_filtered.groupby('temp_category')['cnt'].mean().reset_index()
    fig_temp, ax_temp = plt.subplots(figsize=(8, 4))
    sns.barplot(x='temp_category', y='cnt', data=temp_cat_avg, palette='magma', ax=ax_temp)
    ax_temp.set_title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
    ax_temp.set_xlabel("Kategori Suhu")
    ax_temp.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig_temp)
    
st.write("Dashboard ini telah menyajikan seluruh hasil analisis dari notebook secara konsisten sesuai dengan pertanyaan bisnis yang ditentukan.")
