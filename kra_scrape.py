import json
import requests
from bs4 import BeautifulSoup
import re

# Obtaining list of URLs to scrape (add the paths relative to the base URL here)


# URL of the website
url = "https://www.kra.go.ke/helping-tax-payers/faqs/"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the specific 'ul' element with class 'nav' within 'div' with class 'sticky-nav'
sticky_nav_div = soup.find('div', class_='sticky-nav')
if sticky_nav_div:
    nav_ul = sticky_nav_div.find('ul', class_='nav')
    if nav_ul:
        # Extract all 'a' tags within this 'ul' element
        links = nav_ul.find_all('a')
        # Get the 'href' attribute from each 'a' tag
        urls = [link['href'] for link in links if 'href' in link.attrs]
        # Print the URLs
        for url in urls:
            print(url)
        

    else:
        print("No 'ul' with class 'nav' found within 'div' with class 'sticky-nav'.")
else:
    print("No 'div' with class 'sticky-nav' found.")
    

    



url_dict = urls
# Base URL of the website
base_url = "https://www.kra.go.ke"

def scrape_url(base_url, urls):
    all_faqs = {}

    for url in urls:
        full_url = f'{base_url}{url}'
        # Send a GET request to fetch the raw HTML content
        response = requests.get(full_url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Debug: print the first 500 characters of the HTML to ensure we have the correct content
        print(f"Scraping {full_url}")
        print(soup.prettify()[:500])

        # Extract all questions and answers
        faq_list = []
        faq_items = soup.find_all('div', class_='grid-item banking')

        # Debug: print the number of faq items found
        print(f"Found {len(faq_items)} FAQ items on {full_url}.")

        for item in faq_items:
            question = item.find('p', class_='title').get_text(strip=True)
            # Debug: print the question found
            print(f"Question: {question}")

            answer_parts = item.find_all('p')[1:]  # Skip the first <p> which is the question
            answer = ' '.join(part.get_text(strip=True) for part in answer_parts)
            # Debug: print the answer found
            print(f"Answer: {answer}")

            faq_list.append({'question': question, 'answer': answer})

        # Extract the section title and format it
        section_title = url.split('/')[-1]
        formatted_title = re.sub(r'[^a-z0-9-]', '', section_title.lower().replace(' ', '-'))
        
        all_faqs[formatted_title] = faq_list

    # Save all FAQs to a JSON file
    with open('FAQ.json', 'w') as json_file:
        json.dump(all_faqs, json_file, indent=4)

    print("FAQ extracted and saved to FAQ.json")

# Run the scraping function
scrape_url(base_url, url_dict)
