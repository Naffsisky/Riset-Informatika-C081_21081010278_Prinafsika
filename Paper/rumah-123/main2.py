import re
import csv

def extract_property_info(text):
    info = {
        'judul': '',
        'harga': '',
        'lokasi': '',
        'kamar_tidur': '',
        'kamar_mandi': '',
        'carport': '',
        'luas_tanah': '',
        'luas_bangunan': ''
    }
    
    # Extract title (first line that's not "Rumah" or "Premier")
    lines = text.split('\n')
    for line in lines:
        if line.strip() and line.strip() not in ["Rumah", "Premier"]:
            info['judul'] = line.strip()
            break
    
    # Extract price
    price_match = re.search(r'Rp\s*[\d,.]+\s*(?:Juta|Miliar)', text)
    if price_match:
        info['harga'] = price_match.group()
    
    # Extract location
    location_match = re.search(r'([^,\n]+),\s*([^,\n]+)', text)
    if location_match:
        info['lokasi'] = location_match.group()
    
    # Extract bedrooms, bathrooms, and carport
    numbers = re.findall(r'\n(\d+)\n', text)
    if len(numbers) >= 3:
        info['kamar_tidur'], info['kamar_mandi'], info['carport'] = numbers[:3]
    elif len(numbers) == 2:
        info['kamar_tidur'], info['kamar_mandi'] = numbers
    
    # Extract land and building area
    lt_match = re.search(r'LT\s*:\s*(\d+)\s*m²', text)
    lb_match = re.search(r'LB\s*:\s*(\d+)\s*m²', text)
    info['luas_tanah'] = f"{lt_match.group(1)} m²" if lt_match else ''
    info['luas_bangunan'] = f"{lb_match.group(1)} m²" if lb_match else ''
    
    return info

def process_csv(input_file_path, output_file_path):
    results = []
    with open(input_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:  # Check if the row is not empty
                listing_text = row[0]  # Assuming each row contains one listing in the first column
                results.append(extract_property_info(listing_text))
    
    # Write results to output CSV file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=results[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(results)
    
    return results

# Example usage
input_csv_file_path = './data_rumah.csv'  # Path to your input CSV file
output_csv_file_path = './processed_data_rumah.csv'  # Path for the output CSV file
results = process_csv(input_csv_file_path, output_csv_file_path)

print(f"Processed {len(results)} listings. Results saved to {output_csv_file_path}")

# Optional: Print the first few results to verify
for i, result in enumerate(results[:3], 1):  # Print first 3 results
    print(f"\nListing {i}:")
    for key, value in result.items():
        print(f"{key}: {value}")