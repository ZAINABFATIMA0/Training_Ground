import factory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Product, Image, Details, Attributes

fake = Faker()

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyFunction(fake.word)
    sku = factory.LazyFunction(lambda: fake.random_number(digits=5))
    price = factory.LazyFunction(lambda: fake.random_number(digits=4))

class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    product = factory.SubFactory(ProductFactory)
    image_url = factory.LazyFunction(fake.image_url)

class DetailsFactory(DjangoModelFactory):
    class Meta:
        model = Details

    product = factory.SubFactory(ProductFactory)
    shirt = factory.LazyFunction(fake.text)
    trouser = factory.LazyFunction(fake.text)
    duppata = factory.LazyFunction(fake.text)

class AttributesFactory(DjangoModelFactory):
    class Meta:
        model = Attributes

    product = factory.SubFactory(ProductFactory)
    color = factory.LazyFunction(fake.color_name)
    fabric = factory.LazyFunction(fake.word)
    disclaimer = factory.LazyFunction(fake.sentence)
