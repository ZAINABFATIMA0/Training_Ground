import json
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    """
    A Scrapy spider for scraping product information from the Junaid Jamshed website.
    """
    name = "J_Scrapper"

    def start_requests(self):
        """
        Initializes the scraping process by sending a request to the base URL.

        The method also sets the cookies necessary for the session.
        """
        urls = [
            "https://www.junaidjamshed.com/",
        ]
        cookies = {
            "PHPSESSID": "fbdda54e23e810eb694fd47ec674226b",
            "wp_ga4_customerGroup": "NOT LOGGED IN",
            "wp_customerGroup": "NOT LOGGED IN",
            "form_key": "kCzQghewDdVFupEB",
            "mage-cache-sessid": "true",
            "_fbp": "fb.1.1719225566466.690616671166363123",
            "mage-messages": "",
            "_gcl_au": "1.1.1846065812.1719225567",
            "__adroll_fpc": "224d841f0b458e7c0dc56b05944ce64b-1719225567487",
            "_hjSession_1369653": "eyJpZCI6ImU5ZjU5YmNkLTdmYTUtNDE0NC04YzA4LTVhZjZjNTIzOTA0MCIsImMiOjE3MTkyMjU1Njc1MjAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=",
            "_tt_enable_cookie": "1",
            "_ttp": "CCrOmtFbWsDsKwXqtd3e0DMADnr",
            "countrycurrency": "PKR",
            "_hjSessionUser_1369653": "eyJpZCI6IjgzNjZkNjYxLTMyMmItNWFkNi1hZGFlLTIyNzE4Y2I3M2E1MyIsImNyZWF0ZWQiOjE3MTkyMjU1Njc1MjAsImV4aXN0aW5nIjp0cnVlfQ==",
            "section_data_ids": "{\"apptrian_tiktok_pixel_matching_section\":1719228197}",
            "private_content_version": "0975d28e1ab7534c2633b7b25b432102",
            "_tracking_consent": "{\"con\":{\"CMP\":{\"a\":\"\",\"m\":\"\",\"p\":\"\",\"s\":\"\"}},\"v\":\"2.1\",\"region\":\"PKPB\",\"reg\":\"\"}",
            "_cmp_a": "{\"purposes\":{\"a\":true,\"p\":true,\"m\":true,\"t\":true},\"display_banner\":false,\"sale_of_data_region\":false}",
            "_shopify_y": "bf79f283-06f8-4f85-b738-c8650e6119f5",
            "_orig_referrer": "https://www.junaidjamshed.com/",
            "_landing_page": "/",
            "_gid": "GA1.2.918343573.1719228933",
            "_shopify_sa_p": "",
            "_shopify_s": "01300662-da43-4d7b-b05f-791226c38888",
            "_shopify_sa_t": "2024-06-24T11:42:22.407Z",
            "_ga_D479ZMQWWW": "GS1.1.1719228933.1.1.1719229345.0.0.0",
            "mage-cache-storage": "{}",
            "mage-cache-storage-section-invalidation": "{}",
            "mage-banners-cache-storage": "{}",
            "recently_viewed_product": "{}",
            "product_data_storage": "{}",
            "recently_viewed_product_previous": "{}",
            "recently_compared_product": "{}",
            "recently_compared_product_previous": "{}",
            "_ga_NZV9RQSHHH": "GS1.2.1719229026.1.1.1719230248.0.0.0",
            "_ga": "GA1.1.1930631762.1719225567",
            "_ga_4NJNWKXG24": "GS1.1.1719227994.2.1.1719230352.60.0.0",
            "__ar_v4": "PHMQTLHYCREY7AZLBUMNJN:20240624:26|K4IO2OKJYVC5PHCOV7ZLLE:20240624:26"
        }
        
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse_root_url, cookies = cookies)

    def parse_root_url(self, response):
        """
        Parses the root URL and extracts collection URLs.

        Saves the root page as an HTML file and initiates requests to the collection URLs.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of the root URL.
        """
        page = response.url.split("/")[-2]
        filename = f"{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        collection_urls= response.css('nav.navigation a::attr(href)').getall()

        for url in collection_urls:
                yield scrapy.Request(url = url, callback = self.parse_collection_urls)
            

    def parse_collection_urls(self, response):     
        """
        Parses collection URLs and extracts product URLs.

        Follows pagination links to navigate through all collection pages.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of a collection page.
        """
        product_links = response.css('h2.product.name.product-item-name a.product-item-link::attr(href)')
        product_urls = product_links.getall()

        for url in product_urls:
            yield scrapy.Request(url = url, callback = self.parse_product_details_url)
        
        next_page = response.css('li.item.pages-item-next a.action.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url = next_page, callback = self.parse_collection_urls)

    def parse_additional_information(self, response):
        """
        Extracts additional information (attributes) from a product detail page.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of a product detail page.

        Returns:
            dict: A dictionary containing additional product attributes.
        """
        additional_information = {}
        product_attributes_rows = response.css('table#product-attribute-specs-table tr')
        for row in product_attributes_rows:
            label = row.css('th::text').get()
            if not label:
                continue
            value = ' '.join(row.css('td *::text').getall()).strip()
            if label and value:
                additional_information[label] = value
        return additional_information

    def parse_sizes(self, response):
        """
        Extracts available sizes for a product from a product detail page.

        Args:
            response (scrapy.http.Response): 
                The response object containing the HTML content of a product detail page.

        Returns:
            list: A list of available sizes for the product.
        """
        size = []
        product_size_script = response.css('script[type="text/x-magento-init"]::text')[8].get()
        
        try:
            productsize = json.loads(product_size_script)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON: {e}")
            return
        
        swatch_options = productsize.get('[data-role=swatch-options]', {})
        size_data = swatch_options.get('Magento_Swatches/js/swatch-renderer', {}).get('jsonSwatchConfig', {})

        for attribute_id, attribute_data in size_data.items():
            for size_option_id, size_option_data in attribute_data.items():
                if isinstance(size_option_data, dict):
                    label = size_option_data.get('label')
                    if label:
                        size.append(label)
                else:
                    self.logger.warning(f"Unexpected data type for option_data: {size_option_data}")
        return size
    
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
        product_name = response.css('h1.page-title span.base::text').get()
        sku = response.css('div.product.attribute.sku div.value::text').get()
        price = response.css('span.price::text').get()
        description_text = response.css('div.product.attribute.overview div.value *::text').getall()
        image_links = response.css('[id^="MagicToolboxSelectors"] a::attr(href)').getall()
        details_text = response.css('div.product.attribute.description div.value *::text').getall()
        additional_information = self.parse_additional_information(response)
        sizes = self.parse_sizes(response)

        yield {
            'product_name': product_name,
            'sku': sku,           
            'price': price,
            'Size/Shades': sizes,
            'description': description_text,
            'details': details_text,
            'additional_attributes': additional_information,
            'Images_URL': image_links,
        }
