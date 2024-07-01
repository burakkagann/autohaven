from django.shortcuts import render, redirect
from .forms import SignUpForm
from .dummy_data import dummy_user_regular, dummy_user_seller, dummy_listings, dummy_orders, dummy_offers

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
    # Pass the dummy user to the template for testing
    context = {
        'user': dummy_user_seller,  # Change to dummy_user_seller to test seller version
        'listings': dummy_listings,
        'orders': dummy_orders,
        'offers': dummy_offers,
    }

    return render(request, 'profile.html', context)