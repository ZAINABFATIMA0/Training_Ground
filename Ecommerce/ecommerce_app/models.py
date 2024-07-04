from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length = 255)
    sku = models.CharField(max_length = 50, unique = True)
    price = models.JSONField()
    description = models.TextField()
    details = models.JSONField(blank = True, null = True)
    color = models.CharField(max_length = 50)
    product_category = models.CharField(max_length = 100)
    season = models.CharField(max_length = 50)
    fabric = models.CharField(max_length = 50)
    disclaimer = models.TextField()

    def __str__(self):
        return self.product_name


class Image(models.Model):
    product = models.ForeignKey(Product, related_name = 'images', on_delete = models.CASCADE)
    image_url = models.URLField(max_length = 500)

    def __str__(self):
        return self.image_url
