from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('home/', views.landing_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('new-listing/', views.new_listing, name='new-listing'),
]