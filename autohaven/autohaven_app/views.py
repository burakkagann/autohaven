import logging
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from .dummy_data import dummy_user_regular, dummy_user_seller, dummy_listings, dummy_orders, dummy_offers

logger = logging.getLogger(__name__)  # Create a logger instance

def root(request):
    return redirect('home')

def about(request):
    return render(request, 'base.html')

def register(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'login.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def catalog_page(request):
    return render(request, 'catalog.html')

def logout(request):
    return render(request, 'landing_page.html')


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