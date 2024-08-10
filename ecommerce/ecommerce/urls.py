from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("clothing_catalogue/", include("clothing_catalogue.urls")),
    path("admin/", admin.site.urls),
]
