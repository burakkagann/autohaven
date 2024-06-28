from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def catalog_page(request):
    return render(request, 'catalog.html')
