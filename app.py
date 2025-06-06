import json   
import os
import pandas as pd
import streamlit as st
import openai
from typing import List, Dict
from datetime import datetime
from PIL import Image

# Konfigurasi halaman
st.set_page_config(page_title="Dasbor Siswa", layout="centered")

# Pastikan path absolut ke file Logo.png
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "assets", "Logo.png")

# Load dan tampilkan logo pixel
logo = Image.open(logo_path)
st.sidebar.image(logo, width=200)

# File penyimpanan
BERKAS_DATA = "data_siswa.json"
BERKAS_LOG = "log_perubahan.json"
openai.api_key = st.secrets["openai_api_key"]

# Fungsi hitung nilai huruf
def hitung_grade(nilai: float) -> str:
    if nilai >= 90:
        return "A"
    elif nilai >= 80:
        return "B"
    elif nilai >= 70:
        return "C"
    elif nilai >= 60:
        return "D"
    else:
        return "F"

# Fungsi simpan dan muat data
def simpan_data(daftar_siswa: List[Dict]) -> None:
    with open(BERKAS_DATA, "w") as f:
        json.dump(daftar_siswa, f, indent=4)

def muat_data() -> List[Dict]:
    data: List[Dict] = []
    if os.path.exists(BERKAS_DATA):
        try:
            with open(BERKAS_DATA, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass
    for s in data:
        if "grade" not in s:
            s["grade"] = hitung_grade(float(s["nilai"]))
    return data

def simpan_log(nama, sebelum, sesudah):
    log = []
    if os.path.exists(BERKAS_LOG):
        with open(BERKAS_LOG, "r") as f:
            try:
                log = json.load(f)
            except:
                pass
    log.append({
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aksi": "Update Nilai",
        "nama": nama,
        "sebelum": sebelum,
        "sesudah": sesudah
    })
    with open(BERKAS_LOG, "w") as f:
        json.dump(log, f, indent=4)

# Tambah siswa
def tambah_siswa(nama: str, nomor_absen: str, nilai: float) -> None:
    daftar_siswa = muat_data()
    if any(s["nomor_absen"] == nomor_absen for s in daftar_siswa):
        st.warning("⚠️ Siswa sudah ada.")
        return
    daftar_siswa.append({"nama": nama, "nomor_absen": nomor_absen, "nilai": nilai, "grade": hitung_grade(nilai)})
    simpan_data(daftar_siswa)
    st.success("✅ Siswa berhasil ditambahkan.")

# Edit nilai siswa
def edit_nilai_siswa():
    daftar_siswa = muat_data()
    if not daftar_siswa:
        st.warning("Tidak ada data siswa.")
        return
    df = pd.DataFrame(daftar_siswa)
    pilihan = st.selectbox("Pilih siswa untuk diedit:", df["nama"] + " - " + df["nomor_absen"])
    if pilihan:
        baris = df[df["nama"] + " - " + df["nomor_absen"] == pilihan].iloc[0]
        nilai_baru = st.number_input(f"Nilai baru untuk {baris['nama']}:", 0.0, 100.0, float(baris["nilai"]))
        if st.button("Simpan Perubahan"):
            for siswa in daftar_siswa:
                if siswa["nomor_absen"] == baris["nomor_absen"]:
                    sebelum = siswa.copy()
                    siswa["nilai"] = nilai_baru
                    siswa["grade"] = hitung_grade(nilai_baru)
                    simpan_log(baris["nama"], sebelum, siswa)
                    break
            simpan_data(daftar_siswa)
            st.success("✅ Nilai berhasil diperbarui.")

# Upload file
def unggah_file(file) -> None:
    try:
        df = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
    except Exception as e:
        st.error(f"❌ Gagal membaca file: {e}")
        return
    if not {"nama", "nomor_absen", "nilai"}.issubset(df.columns):
        st.error("❌ Kolom harus ada: 'nama', 'nomor_absen', 'nilai'.")
        return
    df = df[["nama", "nomor_absen", "nilai"]].dropna()
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce")
    df.dropna(subset=["nilai"], inplace=True)
    df["grade"] = df["nilai"].apply(hitung_grade)
    data_baru = df.to_dict(orient="records")
    daftar_siswa = muat_data()
    semua_absen = {s["nomor_absen"] for s in daftar_siswa}
    tambahan = [s for s in data_baru if s["nomor_absen"] not in semua_absen]
    daftar_siswa.extend(tambahan)
    simpan_data(daftar_siswa)
    st.success(f"✅ Ditambahkan: {len(tambahan)} siswa.")

# Unduh data

def unduh_csv() -> bytes:
    daftar_siswa = muat_data()
    if not daftar_siswa:
        return b""
    return pd.DataFrame(daftar_siswa).to_csv(index=False).encode("utf-8")

def unduh_excel() -> bytes:
    daftar_siswa = muat_data()
    if not daftar_siswa:
        return b""
    from io import BytesIO
    buffer = BytesIO()
    pd.DataFrame(daftar_siswa).to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return buffer.read()

# Statistik
def tampilkan_statistik():
    daftar_siswa = muat_data()
    if not daftar_siswa:
        st.info("Tidak ada data.")
        return
    df = pd.DataFrame(daftar_siswa)
    query = st.text_input("🔍 Cari siswa (opsional):")
    if query:
        df = df[df["nama"].str.contains(query, case=False, na=False)]
    st.metric("Total Siswa", len(df))
    st.metric("Rata-rata Nilai", round(df["nilai"].mean(), 2))
    st.subheader("Distribusi Grade")
    st.bar_chart(df["grade"].value_counts().sort_index())

# Ranking
def tampilkan_ranking():
    df = pd.DataFrame(muat_data())
    query = st.text_input("🔍 Cari siswa berdasarkan nama:")
    if query:
        df = df[df["nama"].str.contains(query, case=False, na=False)]
    df = df.sort_values(by="nilai", ascending=False).reset_index(drop=True)
    df.index += 1
    st.dataframe(df[["nama", "nomor_absen", "nilai", "grade"]])

# Filter nilai
def filter_nilai():
    daftar_siswa = muat_data()
    if not daftar_siswa:
        st.warning("Tidak ada data siswa.")
        return
    df = pd.DataFrame(daftar_siswa)
    min_val, max_val = st.slider("Filter berdasarkan rentang nilai:", 0, 100, (60, 100))
    hasil = df[(df["nilai"] >= min_val) & (df["nilai"] <= max_val)]
    st.dataframe(hasil)

# Saran belajar AI
def saran_belajar_ai(nama: str, grade: str, nilai: float) -> str:
    prompt = f"Seorang siswa bernama {nama} mendapatkan nilai {nilai} dan grade '{grade}'. Berikan saran belajar dalam Bahasa Indonesia."
    try:
        hasil = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        return hasil["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Gagal AI: {e}"

def tampilkan_saran_ai():
    daftar_siswa = muat_data()
    if not daftar_siswa:
        st.warning("Data kosong.")
        return
    df = pd.DataFrame(daftar_siswa)
    pilihan = st.selectbox("Pilih siswa", df["nama"] + " - " + df["nomor_absen"])
    if pilihan:
        baris = df[df["nama"] + " - " + df["nomor_absen"] == pilihan].iloc[0]
        st.write(f"Nama: {baris['nama']} | Nilai: {baris['nilai']} | Grade: {baris['grade']}")
        if baris['grade'] == 'A':
            st.success("🏅 Luar biasa! Kamu mendapatkan grade A.")
        if st.button("💡 Dapatkan Saran AI"):
            st.write(saran_belajar_ai(baris['nama'], baris['grade'], baris['nilai']))
        if st.button("👤 Lihat Profil Siswa"):
            st.markdown(f"""
                **Nama:** {baris['nama']}  
                **Nomor Absen:** {baris['nomor_absen']}  
                **Nilai:** {baris['nilai']}  
                **Grade:** {baris['grade']}
            """)

st.title("📚 Dasbor Siswa")

st.header("Tambah Siswa Baru")
with st.form("form_tambah"):
    nama = st.text_input("Nama")
    nomor_absen = st.text_input("Nomor Absen")
    nilai = st.number_input("Nilai Ujian (0-100)", 0.0, 100.0, step=0.1)
    if st.form_submit_button("Tambah"):
        if nama and nomor_absen:
            tambah_siswa(nama, nomor_absen, nilai)
        else:
            st.error("Lengkapi semua kolom.")

st.header("📈 Statistik Nilai")
tampilkan_statistik()

# Menu samping
st.sidebar.title("☰ Menu Navigasi")
pilihan = st.sidebar.radio("Pilih Menu", ["Unggah File", "Lihat Ranking", "Filter Nilai", "Edit Nilai", "Saran Belajar AI", "Hapus Semua Data"])

st.sidebar.markdown("### 📥 Unduh Data Siswa")
data_csv = unduh_csv()
data_excel = unduh_excel()
if data_csv:
    st.sidebar.download_button("Download CSV", data=data_csv, file_name="data_siswa.csv", mime="text/csv")
if data_excel:
    st.sidebar.download_button("Download Excel", data=data_excel, file_name="data_siswa.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if pilihan == "Unggah File":
    berkas = st.sidebar.file_uploader("Unggah File CSV/XLSX", type=["csv", "xlsx"])
    if berkas:
        unggah_file(berkas)

elif pilihan == "Lihat Ranking":
    st.subheader("🏅 Ranking Nilai Siswa")
    tampilkan_ranking()

elif pilihan == "Filter Nilai":
    st.subheader("🔍 Filter Siswa berdasarkan Nilai")
    filter_nilai()

elif pilihan == "Edit Nilai":
    st.subheader("✏️ Edit Nilai Siswa")
    edit_nilai_siswa()

elif pilihan == "Saran Belajar AI":
    st.subheader("🎓 Saran Belajar dari AI")
    tampilkan_saran_ai()

elif pilihan == "Hapus Semua Data":
    if st.sidebar.button("Hapus Sekarang"):
        simpan_data([])
        st.sidebar.success("✅ Semua data telah dihapus.")

