import pandas as pd
import re

# Muat data dari file CSV
df = pd.read_csv('5000_raw-rumah123.csv')

# Fungsi untuk mengonversi string harga menjadi angka
def konversi_harga(harga):
    harga = str(harga).replace("Rp ", "")  # Menghapus simbol "Rp "
    if "Miliar" in harga:
        return float(re.sub(r'[^\d.]', '', harga)) * 1_000_000_000
    elif "Juta" in harga:
        return float(re.sub(r'[^\d.]', '', harga)) * 1_000_000
    return None

# Menerapkan fungsi ke kolom 'Harga'
df['Harga'] = df['Harga'].apply(konversi_harga)

# Simpan hasil ke file CSV baru jika diperlukan
df.to_csv('convert-5000-data.csv', index=False)

print(df.head())  # Tampilkan beberapa baris pertama untuk verifikasi