from django.contrib import admin

from .models import Product, Image, Details, Attributes

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Details)
admin.site.register(Attributes)
