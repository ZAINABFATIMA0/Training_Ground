from django.core.management.base import BaseCommand

from ...factories import ProductFactory, ImageFactory, DetailsFactory, AttributesFactory


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for _ in range(100):
            product_object = ProductFactory()

            for _ in range(3):
                ImageFactory(product=product_object)

            DetailsFactory(product=product_object)
            
            AttributesFactory(product=product_object)

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
