from django.core.management.base import BaseCommand
from faker import Faker

from ...models import Product, Image, Details, Additional_attributes


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(100):
            product = Product.objects.create(
                name=fake.word(),
                sku=fake.random_number(digits=5),
                price=fake.random_number(digits=4)
            )

            for _ in range(3): 
                Image.objects.create(
                    product=product,
                    image_url=fake.image_url()
                )

            Details.objects.create(
                product=product,
                shirt=fake.text(),
                trouser=fake.text(),
                duppata=fake.text()
            )

            Additional_attributes.objects.create(
                product=product,
                color=fake.color_name(),
                fabric=fake.word(),
                disclaimer=fake.sentence()
            )

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
