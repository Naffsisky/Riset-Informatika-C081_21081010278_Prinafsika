import pandas as pd

# Muat data dari file CSV
df = pd.read_csv('convert-5000-data.csv')

# Konversi kolom Tanggal ke format datetime
df_kamar2 = df[df['Kamar_Tidur'] == 2.0]

# Hitung rata-rata harga
rata_rata_harga_kamar2 = df_kamar2['Harga'].mean()

print(f"Rata-rata harga rumah dengan 2 kamar tidur adalah: Rp {rata_rata_harga_kamar2:,.2f}")