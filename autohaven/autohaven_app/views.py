from django.shortcuts import render
from .dummy_data import dummy_user_regular, dummy_user_seller, dummy_listings, dummy_orders, dummy_offers

def profile(request):
    # Pass the dummy user to the template for testing
    context = {
        'user': dummy_user_seller,  # Change to dummy_user_seller to test seller version
        'listings': dummy_listings,
        'orders': dummy_orders,
        'offers': dummy_offers,
    }

    return render(request, 'profile.html', context)