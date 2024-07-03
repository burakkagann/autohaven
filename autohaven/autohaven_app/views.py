import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, NewListingForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from .dummy_data import dummy_user_regular, dummy_user_seller, dummy_listings, dummy_orders, dummy_offers
from django.core.paginator import Paginator
from .models import Listing, Offer


# logger = logging.getLogger(__name__)  # Create a logger instance

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

@login_required()
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
        'listings_page_obj': listings_page_obj,
        'offers_page_obj': offers_page_obj,
        'listings': dummy_listings,
        'orders': dummy_orders,
        'offers': dummy_offers,
    }

    return render(request, 'profile/index.html', context)

        

#User Authentication Views 

def login_view(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']



        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request)
            #superuser
            if user.is_superuser:
                
                return redirect('/profile/')
            #seller
            elif user.groups.filter(name='Sellers').exists():

                return redirect('/profile/')
            #regular user
            else:
                
                return redirect('/')
        else:
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'login.html', {'error': error_message})
            
        
    return render(request, 'login.html')


def logout_view(request):
        logout(request)
        return redirect('login')


def new_listing(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        form.user = request.user
        if(form.is_valid()):
            newListing = form.save()
            print("newListing", newListing)
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = NewListingForm()
    return render(request, 'profile/create_edit_listing.html', { 'form': form })