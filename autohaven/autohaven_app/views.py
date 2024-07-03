from django.shortcuts import render, redirect
from .forms import SignUpForm
from .dummy_data import dummy_user_regular, dummy_user_seller, dummy_listings, dummy_orders, dummy_offers
from django.core.paginator import Paginator
from .models import Listing, Offer


def root(requst):
    return redirect('home/')

def about(request):
    return render(request, 'base.html')


def login(request):
    return render(request, 'login.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def catalog_page(request):
    return render(request, 'catalog.html')

def logout(request):
    return render(request, 'landing_page.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form })

def profile(request):
    # Listings
    listings = Listing.objects.all()
    listingsPaginator = Paginator(listings, 5)  # Show 10 listings per page.

    listings_page_number = request.GET.get("listings_page")
    listings_page_obj = listingsPaginator.get_page(listings_page_number)

    # Offers made by user
    offers = Offer.objects.all()
    offersPaginator = Paginator(offers, 10)  # Show 10 offers per page.

    offers_page_number = request.GET.get("orders_page")
    offers_page_obj = offersPaginator.get_page(offers_page_number)


    # Pass the dummy user to the template for testing
    context = {
        'user': dummy_user_seller,  # Change to dummy_user_seller to test seller version
        'listings_page_obj': listings_page_obj,
        'offers_page_obj': offers_page_obj,
        'listings': dummy_listings,
        'orders': dummy_orders,
        'offers': dummy_offers,
    }

    return render(request, 'profile/index.html', context)


def new_listing(request):
    return render(request, 'profile/create_edit_listing.html')