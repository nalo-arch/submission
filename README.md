
# Proyek Analisis Data: Bike Sharing Dashboard

Proyek ini merupakan proyek akhir dari kelas Analisis Data dengan Python. Proyek ini bertujuan untuk melakukan analisis menyeluruh pada dataset Bike Sharing dan membuat dashboard interaktif menggunakan Streamlit.

## Deskripsi Proyek

Dalam proyek ini, analisis dilakukan dengan langkah-langkah:
- **Data Wrangling:** Pengumpulan, pemeriksaan, dan pembersihan data menggunakan dataset *day.csv* dan *hour.csv*.
- **Exploratory Data Analysis (EDA):** Analisis statistik deskriptif, visualisasi data, dan analisis korelasi untuk memahami pola penyewaan sepeda.
- **Visualization & Explanatory Analysis:** Membuat visualisasi interaktif untuk menjawab dua pertanyaan bisnis utama:
  1. Bagaimana distribusi penyewaan sepeda sepanjang hari, dan perbedaan antara hari kerja dan akhir pekan?
  2. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?
- **Analisis Lanjutan:** Pengelompokkan data berdasarkan kategori suhu, kelembapan, dan slot waktu untuk menggali insight lebih mendalam.
- **Dashboard:** Implementasi dashboard interaktif dengan Streamlit untuk menampilkan grafik, tabel, dan insight dari analisis.

## Struktur Folder
submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt

## Cara Menjalankan Proyek
1. **Instalasi Dependencies:**
   Pastikan Python sudah terinstal, kemudian jalankan perintah berikut di terminal:
pip install -r requirements.txt


2. **Menjalankan Dashboard:**
Untuk menjalankan dashboard, jalankan perintah berikut di terminal:
streamlit run dashboard/dashboard.py


3. **Dashboard Interaktif:**
Dashboard akan menampilkan visualisasi tren penyewaan sepeda, analisis per hari, dan pengaruh kondisi cuaca.

4. **Deployment:**
Proyek ini dapat dideploy ke Streamlit Cloud. URL deployment dapat ditemukan di file `url.txt`.

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama.
- **Pandas & Numpy**: Untuk manipulasi data.
- **Matplotlib & Seaborn**: Untuk visualisasi data.
- **Streamlit**: Untuk membuat dashboard interaktif.

## Referensi

Proyek ini dibangun dengan mengikuti panduan dan template dari Dicoding:
- [Tutorial Data Wrangling](https://www.dicoding.com/academies/555/tutorials/30980)
- [Tutorial Assessing Data](https://www.dicoding.com/academies/555/tutorials/30985)
- [Tutorial Cleaning Data](https://www.dicoding.com/academies/555/tutorials/30990)
- [Tutorial Exploratory Data Analysis](https://www.dicoding.com/academies/555/tutorials/31095)
- [Tutorial Visualization & Explanatory Analysis](https://www.dicoding.com/academies/555/tutorials/31130)
- [Tutorial Analisis Lanjutan](https://www.dicoding.com/academies/555/tutorials/31135)

## Catatan

Pastikan seluruh file proyek sudah disimpan dengan benar di Google Drive dan diupload ke GitHub untuk deployment ke Streamlit Cloud.
