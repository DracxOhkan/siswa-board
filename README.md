# 📚 Siswa Board

**Siswa Board** adalah aplikasi dashboard interaktif berbasis Streamlit yang memudahkan guru atau pengajar untuk mencatat, mengelola, dan menganalisis nilai siswa secara cepat dan modern. Aplikasi ini juga didukung oleh kecerdasan buatan dari OpenAI untuk memberikan saran belajar yang dipersonalisasi berdasarkan performa siswa.

---

## 🎯 Latar Belakang & Tujuan

Manajemen data siswa seringkali dilakukan secara manual melalui Excel atau catatan kertas. Hal ini rentan terhadap kesalahan, sulit dilacak, dan kurang efisien. Oleh karena itu, aplikasi ini hadir untuk:

- Menyediakan tampilan visual data siswa yang menarik.
- Menghitung nilai huruf (grade) secara otomatis.
- Memberikan insight dari AI untuk peningkatan belajar siswa.
- Mempermudah ekspor dan impor data dalam berbagai format.

---

## 🚀 Fitur-Fitur Utama

- ✅ **Tambah siswa baru** secara manual atau melalui file Excel/CSV
- ✏️ **Edit nilai siswa** dan otomatis update grade
- 📊 **Statistik & visualisasi nilai** dalam bentuk metrik & chart
- 🏆 **Ranking siswa** berdasarkan nilai tertinggi
- 🔍 **Filter berdasarkan nilai atau nama**
- 🎓 **Saran belajar AI dari ChatGPT (via OpenAI API)**
- 📥 **Export data** ke format CSV atau Excel
- 🌙 **Tampilan sidebar gelap dengan logo & brand custom**

---

## 🖥️ Cara Menjalankan Aplikasi di Lokal

### 1. Clone Repository
```bash
git clone https://github.com/namakamu/siswa-board.git
cd siswa-board
```

### 2. Install Library
Pastikan kamu sudah mengaktifkan virtual environment (opsional), lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Tambahkan API Key (OpenAI)
Buat file `.streamlit/secrets.toml` lalu isi:
```toml
openai_api_key = "ISI_API_KAMU"
```

### 4. Jalankan Aplikasi
```bash
streamlit run siswa_board_app.py
```

---

## 🖼️ Preview Aplikasi

![Preview Dashboard](![image](https://github.com/user-attachments/assets/4190e10e-4700-468d-bab0-5a554ddc0932)


---

## 🌐 Link Deploy

Aplikasi ini dapat diakses langsung di:
👉 [https://siswa-board.streamlit.app](https://siswa-board.streamlit.app)  
*(Jika belum aktif, kamu bisa deploy sendiri di [streamlit.io/cloud](https://streamlit.io/cloud))*

---

## 🛠️ Daftar Kebutuhan (requirements.txt)

```text
streamlit==1.35.0
pandas==2.2.2
openai==1.30.3
pillow==10.3.0
```

---

## ❤️ Kontribusi & Lisensi

Kamu bebas memodifikasi, membagikan, dan mengembangkan proyek ini untuk kebutuhan pendidikan. Jangan lupa kasih ⭐ di GitHub kalau kamu terbantu!
