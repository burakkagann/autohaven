from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.root),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('home/', views.landing_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]