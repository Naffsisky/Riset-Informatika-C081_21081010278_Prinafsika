import pandas as pd
import csv



# Membaca data dari file CSV
input_file = 'data_rumah.csv'  # Ganti dengan nama file CSV Anda
data_raw = pd.read_csv(input_file, header=None, quoting=csv.QUOTE_NONE)[0].tolist()

# List untuk menyimpan data yang sudah dibersihkan
cleaned_data = []

for entry in data_raw:
    # Ekstraksi informasi menggunakan regex
    title_match = re.search(r'(Rumah [\w\s]+)', entry)
    price_match = re.search(r'(Rp [\d,.]+)', entry)
    location_match = re.search(r'([A-Za-z\s,]+(?:, [A-Za-z\s]+)?)\s+\d+\s+\d+\s+LT', entry)
    bedrooms_match = re.search(r'(\d+)\s+\d+\s+LT', entry)
    bathrooms_match = re.search(r'(\d+)\s+LT', entry)
    carport_match = re.search(r'(\d+)\s+LT', entry)
    land_area_match = re.search(r'LT\s*:\s*([\d\s]+m²)', entry)
    building_area_match = re.search(r'LB\s*:\s*([\d\s]+m²)', entry)

    cleaned_data.append({
        'judul': title_match.group(1) if title_match else None,
        'harga': price_match.group(1) if price_match else None,
        'lokasi': location_match.group(1) if location_match else None,
        'kamar_tidur': bedrooms_match.group(1) if bedrooms_match else None,
        'kamar_mandi': bathrooms_match.group(1) if bathrooms_match else None,
        'carport': carport_match.group(1) if carport_match else None,
        'luas_tanah': land_area_match.group(1) if land_area_match else None,
        'luas_bangunan': building_area_match.group(1) if building_area_match else None
    })

# Membuat DataFrame dari data yang sudah dibersihkan
df = pd.DataFrame(cleaned_data)

# Menyimpan data yang sudah dibersihkan ke file CSV
output_file = 'data_cleaned.csv'  # Nama file output
df.to_csv(output_file, index=False)

print(f"Data telah dibersihkan dan disimpan sebagai '{output_file}'")
