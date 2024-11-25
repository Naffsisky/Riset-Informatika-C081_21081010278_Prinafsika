import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Muat data dari file CSV
df = pd.read_csv('convert-5000-data.csv')

# Mengelompokkan data berdasarkan lokasi dan menghitung jumlah penjualan serta harga rata-rata
daerah_summary = df.groupby('Lokasi').agg(
    jumlah_penjualan=('Lokasi', 'size'),
    rata_rata_harga=('Harga', 'mean')
).reset_index()

# Sortir data berdasarkan jumlah penjualan tertinggi
daerah_summary = daerah_summary.sort_values(by='jumlah_penjualan', ascending=False)

# Plot visualisasi
plt.figure(figsize=(12, 8))
sns.barplot(data=daerah_summary.head(10), x='jumlah_penjualan', y='Lokasi', palette='viridis')
plt.xlabel('Jumlah Penjualan')
plt.ylabel('Lokasi')
plt.title('Top 10 Lokasi dengan Penjualan Terbanyak')
plt.show()

# Visualisasi harga rata-rata per daerah
plt.figure(figsize=(12, 8))
sns.barplot(data=daerah_summary.head(10), x='rata_rata_harga', y='Lokasi', palette='magma')
plt.xlabel('Harga Rata-Rata (Rupiah)')
plt.ylabel('Lokasi')
plt.title('Top 10 Lokasi dengan Harga Rata-Rata Tertinggi')
plt.show()