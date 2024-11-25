import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL and headers
base_url = "https://www.rumah123.com/jual/banten/rumah/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

# Function to get the house listing data
def get_house_data(page_num):
    url = f"{base_url}?page={page_num}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    houses = []
    
    # Find all the cards (you may need to adjust the selector)
    listings = soup.find_all('div', class_='ui-organism-intersection__element intersection-card-container')
    
    for listing in listings:
        try:
            # Safely extract title, price, location, etc., with conditional checks
            title = listing.find('a').get_text().strip() if listing.find('a') else "No title"
            price = listing.find('div', class_='card-featured__middle-section__price').get_text().strip() if listing.find('div', class_='card-featured__middle-section__price') else "No price"
            location = listing.find('span').get_text().strip() if listing.find('span') else "No location"
            
            # Extract other attributes like size, bedrooms, bathrooms, etc.
            size_lt = listing.find('div', string='LT :').find_next('span').get_text() if listing.find('div', string='LT :') else "No LT"
            size_lb = listing.find('div', string='LB :').find_next('span').get_text() if listing.find('div', string='LB :') else "No LB"

            bedrooms = listing.find('svg', {'xlink:href': '#rui-icon-bed-small'}).find_next('span').get_text() if listing.find('svg', {'xlink:href': '#rui-icon-bed-small'}) else "No bedrooms"
            bathrooms = listing.find('svg', {'xlink:href': '#rui-icon-bath-small'}).find_next('span').get_text() if listing.find('svg', {'xlink:href': '#rui-icon-bath-small'}) else "No bathrooms"

            cars = listing.find('svg', {'xlink:href': '#rui-icon-car-small'}).find_next('span').get_text() if listing.find('svg', {'xlink:href': '#rui-icon-car-small'}) else "No car slots"

            houses.append({
                'title': title,
                'price': price,
                'location': location,
                'size_lt': size_lt,
                'size_lb': size_lb,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'cars': cars
            })
        except Exception as e:
            print(f"Error occurred while parsing a listing: {e}")
    
    return houses

# Scrape multiple pages
def scrape_all_pages(max_pages=20):
    all_houses = []
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        houses_on_page = get_house_data(page)
        if houses_on_page:
            all_houses.extend(houses_on_page)
        else:
            print(f"No more listings found on page {page}. Stopping.")
            break

    return all_houses

# Scrape data and save to CSV
houses = scrape_all_pages(max_pages=20)
df = pd.DataFrame(houses)
df.to_csv('rumah123_banten_listings.csv', index=False)
print("Data saved to rumah123_banten_listings.csv")