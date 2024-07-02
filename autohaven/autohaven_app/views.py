from django.shortcuts import render, redirect
from .forms import SignUpForm
from .dummy_data import dummy_user_regular, dummy_user_seller, dummy_listings, dummy_orders, dummy_offers
from django.core.paginator import Paginator
from .models import Listing, Offer
from .forms import UserUpdateForm 
from django.contrib.auth.models import User

def root(requst):
    return redirect('home/')

def about(request):
    return render(request, 'navbar/header.html')

def register(request):
    return render(request, 'navbar/header.html')

def login(request):
    return render(request, 'login.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def catalog_page(request):
    return render(request, 'catalog.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form })


def profile(request):
    #User
    #user = request.user    #This will be changed with the code below when login system is activated. For now it gives AnonymousUser. 
    user = User.objects.get(username='regularuser') # Change username for testing other users type like : regularuser, seller, superuser!!

    is_regular_user = user.groups.filter(name='RegularUsers').exists()
    is_seller = user.groups.filter(name='Sellers').exists()
    is_super_user = user.groups.filter(name='SuperUsers').exists()

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same page after saving. Change for other redirects
    else:
        form = UserUpdateForm(instance=user)

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

    context = {
        'form': form,
        'user': user,
        'is_regular_user': is_regular_user,
        'is_seller': is_seller,
        'is_super_user': is_super_user,
        'listings_page_obj': listings_page_obj,
        'offers_page_obj': offers_page_obj,
        'offers': dummy_offers,
    }

    return render(request, 'profile/index.html', context)


def new_listing(request):
    return render(request, 'profile/create_edit_listing.html')