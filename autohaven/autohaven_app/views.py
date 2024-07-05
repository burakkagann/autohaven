import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm
from . import models
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from .dummy_data import dummy_offers
from django.core.paginator import Paginator
from .models import Listing, Offer, SellerUser
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
    # Pull Listing from models (databse)
    listing = models.Listing.objects.all()

    # Filter Listings
    brand_filter = request.GET.get('brand')
    model_filter = request.GET.get('model')
    year_filter = request.GET.get('year')
    body_type_filter = request.GET.get('body_type')
    engine_type_filter = request.GET.get('engine_type')
    mileage_filter = request.GET.get('mileage')
    price_filter = request.GET.get('price')
    offering_type_filter = request.GET.get('offering_type')

    # Apply filters
    if brand_filter:
        listing = listing.filter(brand=brand_filter)

    if model_filter:
        listing = listing.filter(model=model_filter)

    if year_filter:
        listing = listing.filter(year__lte=year_filter)

    if body_type_filter:
        listing = listing.filter(body_type=body_type_filter)

    if engine_type_filter:
        listing = listing.filter(engine_type=engine_type_filter)

    if mileage_filter:
        listing = listing.filter(mileage__lte=mileage_filter)

    if price_filter:
        listing = listing.filter(price__lte=price_filter)

    if offering_type_filter:
        listing = listing.filter(type=offering_type_filter)

    # Match  filtered listings to according images
    listing_with_images = []
    for item in listing:
        images = models.ListingImage.objects.filter(listing=item)
        first_image = images.first()
        listing_with_images.append({
            'listing': item,
            'image': first_image
        })

    # Get Filter Value Fields
    brand = models.Listing.objects.values('brand').distinct()
    model = models.Listing.objects.values('model').distinct()
    year = models.Listing.objects.values('year').distinct()
    body_type = models.Listing.objects.values('body_type').distinct()
    engine_type = models.Listing.objects.values('engine_type').distinct()


    return render(request, 'catalog.html', {
        'listing': listing_with_images,
        'brand': brand,
        'model': model,
        'year': year,
        'body_type': body_type,
        'engine_type': engine_type})

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
    user = request.user

    is_regular_user = user.groups.filter(name='RegularUsers').exists()
    is_seller = user.groups.filter(name='Sellers').exists()
    is_super_user = user.groups.filter(name='SuperUsers').exists()

  
    seller_user = SellerUser.objects.get_or_create(user=user)[0] if is_seller else None

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if is_seller and seller_user:
                 seller_user.company_name = request.POST.get('company_name', '')
                 seller_user.save()
            return redirect('profile')  # Redirect to the same page after saving. Change for other redirects
    else:
        form = UserUpdateForm(instance=user)

    # Listings
       
    if is_super_user:
        listings = Listing.objects.all()
    else:
        listings = Listing.objects.filter(user=user) 
    
    #listings = Listing.objects.all() #this can be used to test listing table instead of above if statement

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
        'seller_user': seller_user,
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
