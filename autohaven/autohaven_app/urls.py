from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.root),
    path('about/', views.about, name='about'),
    path('home/', views.landing_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('new-listing/', views.new_listing, name='new-listing'),
    path('manage-listing/<int:listingId>', views.manage_listing, name='manage-listing'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing_page.html'), name='logout'),
    path('sellers/upload/', views.upload_new_seller, name='upload_new_seller'),
    path('sellers/manage/<int:id>/', views.manage_seller, name='manage_seller'),
]
