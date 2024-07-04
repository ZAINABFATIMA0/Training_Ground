from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("ecommerce_app/", include("ecommerce_app.urls")),
    path("admin/", admin.site.urls),
]
