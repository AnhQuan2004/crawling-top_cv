import cloudscraper
import json
import time
import random

# Path to the text file containing the URLs
input_file_path = 'extracted_urls.txt'

# Path to save the output JSON file
output_file_path = 'urls_and_html.json'

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

# Function to handle the request and retry on 429
def get_html_with_retry(url, headers, retries=3):
    for attempt in range(retries):
        response = scraper.get(url, headers=headers)

        # If the request is successful, return the HTML content
        if response.status_code == 200:
            return response.text

        # If 429, wait and retry
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 30))  # Default wait time if not provided
            print(f"Rate limit reached for {url}. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)

        # For other errors, stop and return None
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return None

    # If we exhausted retries and still failed
    print(f"Max retries exceeded for {url}. Skipping.")
    return None

try:
    # Open the file containing URLs
    with open(input_file_path, 'r') as file:
        urls = file.readlines()

    # Loop through each URL and get the HTML
    for url in urls:
        url = url.strip()  # Remove any extra whitespace/newline characters
        if url:
            try:
                # Add a random delay between requests to avoid being blocked
                time.sleep(random.uniform(5, 15))

                # Get the HTML content with retries on 429
                html_content = get_html_with_retry(url, headers)

                if html_content:
                    # Create the dictionary for the current URL and HTML
                    data = {
                        'url': url,
                        'html': html_content
                    }

                    # Open the JSON file in append mode and save the current data (compact format)
                    with open(output_file_path, 'a', encoding='utf-8') as json_file:
                        json_file.write(json.dumps(data, ensure_ascii=False) + '\n')

                    print(f"Successfully retrieved and saved HTML for: {url}")

            except Exception as e:
                print(f"An error occurred while processing {url}: {str(e)}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
