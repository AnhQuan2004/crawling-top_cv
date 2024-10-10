import cloudscraper
from bs4 import BeautifulSoup
import time
import random

# Base URL of the website you want to scrape
base_url = 'https://www.topcv.vn/tim-viec-lam-frontend?sba=1&page='

# Create a scraper instance
scraper = cloudscraper.create_scraper(browser='chrome')

# Add custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.topcv.vn/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Path to save the URLs to a text file
file_output_path = 'extracted_urls.txt'

# Define the range of pages you want to scrape
start_page = 1
end_page = 3

try:
    # Open the file to save the URLs
    with open(file_output_path, 'w') as file:
        # Loop through each page
        for i in range(start_page, end_page + 1):
            # Construct the URL for each page
            url = f'{base_url}{i}'

            # Add a random delay before making the request
            time.sleep(random.uniform(2, 5))

            # Send a GET request for each page
            response = scraper.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all <a> tags within elements that have the class "title"
                title_links = soup.select('.title a')

                # Extract URLs and save to the text file
                for link in title_links:
                    href = link.get('href')
                    if href:
                        file.write(href + '\n')
                        print(href)  # Optional: print each URL to the console

            else:
                print(f"Failed to retrieve page {i}. Status code: {response.status_code}")

    print(f"URLs successfully saved to {file_output_path}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
