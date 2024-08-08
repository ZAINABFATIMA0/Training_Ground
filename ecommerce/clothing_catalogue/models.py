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
    
    shirt = models.TextField(blank=True, null=True)
    trouser = models.TextField(blank=True, null=True)
    duppata = models.TextField(blank=True, null=True)


class Attributes(models.Model):
    product = models.ForeignKey(
        Product, related_name='attributes', on_delete=models.CASCADE
        )
    
    color = models.CharField(max_length=50)
    fabric = models.CharField(max_length=50)
    disclaimer = models.CharField(max_length=50)




"""
URL configuration for eventify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("events/", include("events.urls")),
    path("communications/", include("communications.urls")),

]


