# Junaid Jamshed Product Scraper

Junaid Jamshed Product Scraper is a Python Scrapy spider for extracting product information from the Junaid Jamshed website.

## Features

- **Scraping Capability:** Extracts product names, SKUs, prices, descriptions, sizes, images, and additional attributes.
- **Cookie Handling:** Initializes scraping with necessary session cookies.
- **Pagination Support:** Follows pagination links to scrape all product pages.
- **Data Extraction:** Parses HTML content to retrieve structured data.
- **JSON Configuration:** Handles JSON data embedded in script tags for dynamic content.

## Setup

1. Ensure you have Python 3.x installed on your system.

2. Clone or download the repository:
   ```bash
   git clone git@github.com:ZAINABFATIMA0/Training_Ground.git
   cd Training_Ground
3. Install Scrapy if not already installed
    ```bash
    pip install scrapy
## Usage
 Run the spider using the following command:
 
    scrapy crawl J_Scrapper -o product.json

## Output

A json-file with all the product information including names, SKUs, prices, sizes, descriptions, images, and additional attributes from the Junaid Jamshed website.


   

