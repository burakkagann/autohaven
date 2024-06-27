from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'navbar/header.html')

def catalog(request):
    return render(request, 'navbar/header.html')

def about(request):
    return render(request, 'navbar/header.html')

def register(request):
    return render(request, 'navbar/header.html')

def login(request):
    return render(request, 'navbar/header.html')

# Create your views here.
