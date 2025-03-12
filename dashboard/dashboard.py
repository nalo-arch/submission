import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Gunakan backend non-interactive
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

@st.cache(allow_output_mutation=True)
def load_data():
    # Baca data dari file main_data.csv
    data = pd.read_csv("dashboard/main_data.csv", parse_dates=["dteday"])
    return data

# Muat data
data = load_data()

st.title("Dashboard Penyewaan Sepeda")
st.write("Dashboard interaktif untuk analisis Bike Sharing")

# Trend Harian Penyewaan Sepeda
st.subheader("Trend Harian Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(data["dteday"], data["cnt"], marker="o", linestyle="-")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Tampilkan Tabel Data (20 baris pertama)
st.subheader("Tabel Data Penyewaan")
st.dataframe(data.head(20))
