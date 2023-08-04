import requests
from bs4 import BeautifulSoup

# Define the URL of the supplier site
url = 'https://www.suppliersite.com'

# Send a GET request to the supplier site
response = requests.get(url)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all product listings on the page
product_listings = soup.find_all('div', class_='product-listing')

# For each product listing, extract the product name and price
for product_listing in product_listings:
    product_name = product_listing.find('h2', class_='product-name').text
    product_price = product_listing.find('span', class_='product-price').text
    print(f'Product Name: {product_name}, Product Price: {product_price}')