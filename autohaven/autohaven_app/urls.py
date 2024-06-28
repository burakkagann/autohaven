from django.urls import path
from . import views

# UrlConf
urlpatterns = [
    path('home/', views.landing_page),
    path('catalog/', views.catalog_page)
]