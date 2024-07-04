import json
from django.core.management.base import BaseCommand
from ecommerce_app.models import Product, Image


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file containing products')

    def load_data_from_json(self, json_file):
        with open(json_file, 'r') as file:
            products = json.load(file)
            for product_data in products:
                image_urls = product_data.get('Images_URL', [])

                product, created = Product.objects.update_or_create(
                    sku=product_data['sku'],
                    defaults={
                        'product_name': product_data['product_name'],
                        'price': product_data['price'],
                        'description': product_data['description'],
                        'details': product_data.get('details', {}),
                        'color': product_data['additional_attributes'].get('Color', ''),
                        'product_category': product_data['category'],
                    }
                )

                product.images.all().delete()
                for image_url in image_urls:
                    Image.objects.create(product=product, image_url=image_url)

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created product {product.product_name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated product {product.product_name}'))
