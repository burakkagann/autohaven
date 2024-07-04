from django.shortcuts import render, redirect
from .forms import SignUpForm
from . import models

def root(requst):
    return redirect('home/')

def about(request):
    return render(request, 'navbar/header.html')

def register(request):
    return render(request, 'navbar/header.html')

def login(request):
    return render(request, 'navbar/header.html')

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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form })
# Create your views here.
