from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', views.root),
    path('about/', views.about, name='about'),
    path('home/', views.landing_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('new-listing/', views.new_listing, name='new-listing'),
    path('manage-listing/<int:listingId>', views.manage_listing, name='manage-listing'),
    path('login/',views.login_user, name='login'),
    path('logout/', views.auth_views.LogoutView.as_view(template_name='landing_page.html'), name='logout'),
    path('sellers/upload/', views.upload_new_seller, name='upload_new_seller'),
    path('sellers/manage/<int:id>/', views.manage_seller, name='manage_seller'),
    path('change-password/', views.auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change-password' ),
    path('password-change-done/', views.password_changed_view.as_view(), name='password_change_done' ),
    path('password-reset/', views.password_reset, name='password-reset'),
    path('password-reset-confirm/<str:username>', views.password_reset_confirm, name='password-reset-confirm'),
    path('catalog/listing/<int:listing_id>/', views.listing_detail, name='listing_detail'), 
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
