import json
from bs4 import BeautifulSoup

# Path to the input JSON file containing URLs and HTML
input_json_file = 'urls_and_html.json'

# Path to save the extracted job data
output_json_file = 'extracted_job_data.json'

# Function to extract job features from HTML content
def extract_job_features(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract job title
    job_title = soup.find(class_='job-detail__info--title')
    job_title = job_title.text.strip() if job_title else None
    
    # Extract company name
    company = soup.find(class_='company-name-label')
    company = company.text.strip() if company else None
    
    # Extract salary
    salary = soup.find(class_='job-detail__info--section-content-value')
    salary = salary.text.strip() if salary else None
    
    # Extract years of experience
    year_of_experience = soup.find(class_='job-detail-info-experience')
    year_of_experience = year_of_experience.text.strip() if year_of_experience else None
    
    # Extract job city (location)
    job_city = soup.find(class_='job-detail__info--section-content-value')
    job_city = job_city.text.strip() if job_city else None
    
    # Extract due date
    due_date = soup.find(class_='job-detail__info--deadline')
    due_date = due_date.text.strip() if due_date else None
    
    # Extract job description
    job_description = soup.find(class_='job-description')
    job_description = job_description.text.strip() if job_description else None
    
    # Return a dictionary with all the extracted information
    return {
        'job_title': job_title,
        'company': company,
        'salary': salary,
        'year_of_experience': year_of_experience,
        'job_city': job_city,
        'due_date': due_date,
        'jd': job_description
    }

# List to store the extracted job data
extracted_data = []

try:
    # Open the JSON file and read each entry
    with open(input_json_file, 'r', encoding='utf-8') as file:
        for line in file:
            entry = json.loads(line)
            url = entry.get('url')
            html_content = entry.get('html')
            
            # Extract job features from the HTML
            job_features = extract_job_features(html_content)
            job_features['url'] = url  # Include the URL in the extracted data
            
            # Add the extracted data to the list
            extracted_data.append(job_features)

    # Save the extracted data to a new JSON file
    with open(output_json_file, 'w', encoding='utf-8') as output_file:
        json.dump(extracted_data, output_file, ensure_ascii=False, indent=4)

    print(f"Extracted job data has been saved to {output_json_file}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
