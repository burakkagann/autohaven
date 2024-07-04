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
    listing_with_images = []

    # Match Listing to according images
    for item in listing:
        images = models.ListingImage.objects.filter(listing=item)
        first_image = images.first()
        listing_with_images.append({
            'listing': item,
            'image': first_image
        })

    # Get Filter Values
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
