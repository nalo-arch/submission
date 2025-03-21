
# Proyek Analisis Data Bike Sharing
```
Proyek ini merupakan proyek akhir untuk kelas Analisis Data yang mengintegrasikan seluruh tahapan proses analisis data mulai dari data wrangling, eksplorasi, hingga visualisasi dan pembuatan dashboard interaktif. Proyek ini menggunakan dataset Bike Sharing untuk menjawab dua pertanyaan bisnis utama:
1. **Bagaimana distribusi penyewaan sepeda sepanjang hari (perbandingan hari kerja vs. akhir pekan)?**
2. **Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?**
Dashboard yang dibuat dengan Streamlit menyediakan fitur interaktif, seperti filter berdasarkan rentang tanggal dan kondisi cuaca, sehingga pengguna dapat mengeksplorasi data secara dinamis.

## Gambaran Proyek
```
Dalam proyek ini, data Bike Sharing diolah melalui beberapa tahap:
- **Data Wrangling & Cleaning:**
  Data awal (day.csv dan hour.csv) diolah untuk menghapus duplikat, mengisi missing values, serta mengkonversi tipe data dan melakukan mapping nilai numerik ke kategori (misalnya, mengubah angka pada kolom weekday menjadi nama hari).
- **Exploratory Data Analysis (EDA):**
  Dilakukan analisis deskriptif dan visualisasi untuk menggali pola-pola penting, seperti tren penyewaan berdasarkan hari dan pengaruh kondisi cuaca terhadap permintaan sepeda.
- **Dashboard Interaktif:**
  Dashboard dibuat menggunakan Streamlit untuk menampilkan dua visualisasi utama yang mendukung kedua pertanyaan bisnis. Fitur interaktif yang disertakan memungkinkan pengguna menyaring data berdasarkan tanggal dan kondisi cuaca.

## Struktur Proyek
```
proyek/
├── dashboard/
│   ├── dashboard.py         # Aplikasi dashboard interaktif dengan Streamlit
│   └── main_data.csv        # Data hasil cleaning (ekspor dari notebook)
├── data/
│   ├── day.csv              # Dataset awal (harian)
│   └── hour.csv             # Dataset awal (per jam)
├── notebooks/
│   └── notebook.ipynb       # Notebook Google Colab berisi proses cleaning, EDA, dan pembuatan file CSV
├── README.md                # Dokumentasi proyek (ini)
└── requirements.txt         # Daftar dependencies untuk proyek
```

## Cara Kerja Proyek
```
Proyek ini dirancang untuk dijalankan dalam dua lingkungan:
### 1. Menggunakan Google Colab
- **Mount Google Drive:**
  Notebook memulai dengan mount Google Drive untuk mengakses dataset dan menyimpan file CSV hasil cleaning.
- **Jalankan Notebook:**
  Buka dan jalankan notebook (`notebook.ipynb`) di Google Colab untuk melakukan proses cleaning dan ekspor data ke `main_data.csv`.
  Contoh kode untuk ekspor:
  ```python
  df_day_cleaned.to_csv('/content/drive/MyDrive/submission/dashboard/main_data.csv', index=False)
  ```
  Pastikan path output sesuai dengan struktur di Google Drive.
### 2. Menjalankan Dashboard dengan Streamlit
- **Pastikan File CSV Tersedia:**
  File `main_data.csv` harus sudah tersimpan di folder `dashboard/` (dapat diperoleh dari hasil eksekusi notebook).
- **Instal Dependencies:**
  Gunakan perintah berikut untuk menginstal paket-paket yang diperlukan:
  ```bash
  pip install -r requirements.txt
  ```
- **Jalankan Aplikasi Secara Lokal:**
  Jalankan dashboard dengan perintah:
  ```bash
  streamlit run dashboard/dashboard.py
  ```

## Deployment ke Streamlit Cloud dengan GitHub
```
Proyek ini juga di-deploy menggunakan GitHub sebagai repositori dan Streamlit Cloud sebagai platform hosting. Berikut langkah-langkahnya:
1. **Push Repository ke GitHub:**
   - Pastikan seluruh file (termasuk `dashboard/dashboard.py`, `dashboard/main_data.csv`, `notebooks/`, `data/`, dan `requirements.txt`) sudah ada di repository GitHub.
   - Commit dan push perubahan ke branch utama (misalnya, `main`).
2. **Hubungkan Repository dengan Streamlit Cloud:**
   - Buka [Streamlit Cloud](https://share.streamlit.io/).
   - Klik **"New App"** dan pilih repository GitHub yang sudah dipush.
   - Tentukan branch (misalnya, `main`) dan main module (`dashboard/dashboard.py`).
   - Klik **"Deploy"** dan tunggu proses build selesai.
3. **Update Jika Diperlukan:**
   Jika ada perubahan pada kode, commit dan push ke GitHub. Streamlit Cloud secara otomatis akan mendeteksi perubahan dan memperbarui aplikasi.
Pastikan bahwa file **requirements.txt** sudah benar dan seluruh file yang dibutuhkan tersedia di repository agar proses deployment berjalan lancar.

## Dependencies
```
File **requirements.txt** mencakup semua paket yang dibutuhkan, antara lain:
```txt
pandas==1.5.3
numpy>=1.24.0,<2.0
matplotlib==3.6.3
seaborn==0.12.2
streamlit==1.18.1
altair==4.2.0
```

## Catatan
```
- **Struktur File:**
  Pastikan struktur folder dan path file sesuai dengan yang tercantum di atas agar tidak terjadi error saat membaca file CSV.
- **Format CSV:**
  File CSV harus dihasilkan dengan perintah `to_csv()` dan berformat valid (header, delimiter, dll) agar dapat diparsing oleh `pd.read_csv()`.
- **Dokumentasi:**
  Setiap langkah proses analisis dan insight yang diperoleh sebaiknya didokumentasikan di dalam notebook untuk memudahkan reviewer memahami proses berpikir.

---

Semoga README ini memberikan gambaran yang jelas mengenai proyek, baik dari sisi analisis data, dashboard interaktif, maupun proses deployment melalui GitHub ke Streamlit Cloud. Jika ada pertanyaan atau perlu bantuan lebih lanjut, silakan hubungi saya melalui email: [agnesanola01@gmail.com].
