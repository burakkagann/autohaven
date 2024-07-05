import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from .dummy_data import dummy_user_regular, dummy_user_seller, dummy_listings, dummy_orders, dummy_offers
from django.core.paginator import Paginator
from .models import Listing, Offer
from .forms import UserUpdateForm 
from django.contrib.auth.models import User

# logger = logging.getLogger(__name__)  # Create a logger instance

def root(request):
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
            return redirect('home')  # Replace 'home' with your actual redirect URL
        # TODO uncomment when the modal popup is ready
            # return render(request, 'signup.html', { 'modal_open': true}) 
            
        else:
            print(form.errors)
    else:
        form = SignUpForm()
        
    # If the form is invalid, render the form with errors
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append(f"{error}")

    return render(request, 'signup.html', {'form': form, 'error_messages': error_messages})


@login_required()
def profile(request):
    #User
    user = request.user    #This will be changed with the code below when login system is activated. For now it gives AnonymousUser. 
    #user = User.objects.get(username='regularuser') # Change username for testing other users type like : regularuser, seller, superuser!!

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
        return redirect('home')


def new_listing(request):
    return render(request, 'profile/create_edit_listing.html')
