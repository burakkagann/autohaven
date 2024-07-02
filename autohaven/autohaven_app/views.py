from django.shortcuts import render, redirect
from .forms import SignUpForm

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
