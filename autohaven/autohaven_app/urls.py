from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.landing_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
]