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
    return render(request, 'catalog.html', {'listing': listing_with_images})


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
