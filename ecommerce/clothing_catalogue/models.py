from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    price = models.JSONField()

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE
        )
    
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return self.image_url
    
    
class Details(models.Model):
    product = models.ForeignKey(
        Product, related_name='details', on_delete=models.CASCADE
        )
    
    shirt = models.TextField(default=None)
    trouser = models.TextField(default=None)
    duppata = models.TextField(default=None)


class Additional_attributes(models.Model):
    product = models.ForeignKey(
        Product, related_name='additional_attributes', on_delete=models.CASCADE
        )
    
    color = models.CharField(max_length=50)
    fabric = models.CharField(max_length=50)
    disclaimer = models.CharField(max_length=50)
