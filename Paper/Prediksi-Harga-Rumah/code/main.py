import requests
import json
import csv
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_nested_value(data, keys, default='N/A'):
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data

def fetch_olx_data(url, limit=100):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_data = []
    page = 1
    
    while len(all_data) < limit:
        current_url = url.replace("page=1", f"page={page}")
        logging.info(f"Fetching data from page {page}")
        
        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('data'):
                logging.info("No more data available. Ending fetch.")
                break
            
            for item in data['data']:
                if len(all_data) >= limit:
                    break
                
                adId = get_nested_value(item, ['ad_id'])
                price = get_nested_value(item, ['price', 'value', 'raw'])
                location = get_nested_value(item, ['locations_resolved', 'SUBLOCALITY_LEVEL_1_name'])
                if location == 'N/A':
                    location = get_nested_value(item, ['locations_resolved', 'ADMIN_LEVEL_3_name'])
                post_date = get_nested_value(item, ['display_date'])
                
                parameters = item.get('parameters', [])
                bedrooms = next((p['formatted_value'] for p in parameters if p['key'] == 'p_bedroom'), 'N/A')
                bathrooms = next((p['formatted_value'] for p in parameters if p['key'] == 'p_bathroom'), 'N/A')
                land_size = next((p['formatted_value'] for p in parameters if p['key'] == 'p_sqr_land'), 'N/A')
                building_size = next((p['formatted_value'] for p in parameters if p['key'] == 'p_sqr_building'), 'N/A')
                
                all_data.append({
                    'Add ID': adId,
                    'Price': price,
                    'Location': location,
                    'Post Date': post_date,
                    'Bedrooms': bedrooms,
                    'Bathrooms': bathrooms,
                    'Land Size': land_size,
                    'Building Size': building_size
                })
                
                logging.info(f"Fetched item {len(all_data)}")
            
            page += 1
            time.sleep(1)  # Small delay between requests
            
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            break
        
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {e}")
            break
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            logging.error(f"Error details: {type(e).__name__}, {str(e)}")
            if 'item' in locals():
                logging.error(f"Problematic item structure: {json.dumps(item, indent=2)}")
            break
    
    return all_data

def save_to_csv(data, filename):
    if not data:
        logging.warning("No data to save.")
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    logging.info(f"Data saved to {filename}")

# URL API OLX
# url = "http://api.olx.co.id/relevance/v4/search?facet_limit=100&clientId=pwa&location_facet_limit=20&relaxedFilters=true&location=2000009&page=1&category=88&clientVersion=11.0.3&user=19284c41a77x6e121efc&platform=web-desktop"

url = "http://api.olx.co.id/relevance/v4/search?category=5158&facet_limit=100&location=5001275&location_facet_limit=20&page=1&clientVersion=11.0.3&user=19284c41a77x6e121efc&platform=web-desktop&relaxedFilters=true&type=rumah&user=19284c41a77x6e121efc"


# Fetch data
start_time = time.time()
fetched_data = fetch_olx_data(url, limit=1000)
end_time = time.time()

# Save results to CSV file
current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f'olx_house_listings_{current_date}.csv'
save_to_csv(fetched_data, filename)

logging.info(f"Data fetching completed. Total time: {end_time - start_time:.2f} seconds")
logging.info(f"Total data fetched: {len(fetched_data)}")