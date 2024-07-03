from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from .models import Listing

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email')


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["brand", "model", "year", "body_type", "engine_type", "mileage", "price", "user"]
