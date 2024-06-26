import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class J_Product_Spider(CrawlSpider):
    """
    A Scrapy spider for scraping product information from the Junaid Jamshed website.
    """
    name = "J_Scrapper"
    allowed_domains = ['junaidjamshed.com']
    start_urls = ['https://www.junaidjamshed.com']

    rules = (
        Rule(
            LinkExtractor(restrict_css = 'li.item.pages-item-next a.action.next'), 
            follow = True
        ),
        Rule(
            LinkExtractor(restrict_css = 'a.product-item-link'),
            callback = 'parse_product_details_url', 
            follow = True
        ),
    )

    def start_requests(self):
        """
        Initializes the scraping process by sending a request to the base URL.

        The method also sets the cookies necessary for the session.
        """
        cookies = {
            "countrycurrency": "PKR",
        }
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse_root_url, cookies = cookies)

    def parse_root_url(self, response):
        """
        Parses the root URL and extracts collection URLs.

        Saves the root page as an HTML file and initiates requests to the collection URLs.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of the root URL.
        """
        product_category_urls = response.css("nav.navigation a::attr(href)").getall()
        for url in product_category_urls:
            yield scrapy.Request(url = url)

    def parse_additional_information(self, response):
        """
        Extracts additional information (attributes) from a product detail page.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of a product detail page.

        Returns:
            dict: A dictionary containing additional product attributes.
        """
        all_product_attributes = response.css("table#product-attribute-specs-table tr")
        additional_information = {
            single_attribute.css("th::text").get(): ' '.join(single_attribute.css("td *::text").getall()).strip()
            for single_attribute in all_product_attributes if single_attribute.css("th::text").get()
        }
        return(additional_information)

    def parse_sizes(self, response):
        """
        Extracts available sizes for a product from a product detail page.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of a product detail page.

        Returns:
            list: A list of available sizes for the product.
        """
        sizes = []
        product_size_data = None
        product_size = response.css("script[type = 'text/x-magento-init']::text").getall()

        for text in product_size:
            if '"Magento_Swatches/js/swatch-renderer"' in text:
                product_size_data = text
                break

        if not product_size_data:
            self.logger.error("Could not find the product size script.")
            return sizes

        try:
            productsize = json.loads(product_size_data)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON: {e}")
            return

        available_sizes_data = productsize.get("[data-role = swatch-options]", {})
        available_sizes = available_sizes_data.get("Magento_Swatches/js/swatch-renderer", {}).get("jsonSwatchConfig", {})

        for attribute_id, attribute_value in available_sizes.items():
            for size_option_id, size_option_value in attribute_value.items():
                if isinstance(size_option_value, dict):
                    size_label = size_option_value.get("label")
                    if size_label:
                        sizes.append(size_label)
                else:
                    self.logger.warning(f"Unexpected data type for option_data: {size_option_value}")
        return sizes

    def parse_product_details_url(self, response):
        """
        Extracts detailed information about a product from a product detail page.

        The information includes product name, SKU, price, description, sizes, and images.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of a product detail page.

        Yields:
            dict: A dictionary containing detailed information about the product.
        """
        product_name = response.css("h1.page-title span.base::text").get()
        sku = response.css("div.product.attribute.sku div.value::text").get()
        price = response.css("span.price::text").get()
        description = response.css("div.product.attribute.overview div.value *::text").getall()
        image_links = response.css("[id^='MagicToolboxSelectors'] a::attr(href)").getall()
        details = response.css("div.product.attribute.description div.value *::text").getall()
        additional_information = self.parse_additional_information(response)
        sizes = self.parse_sizes(response)

        yield {
            "product_name": product_name,
            "sku": sku,
            "price": price,
            "Size/Shades": sizes,
            "description": description,
            "details": details,
            "additional_attributes": additional_information,
            "Images_URL": image_links,
        }
