from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.forms import inlineformset_factory
from .models import Listing, ListingImage

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email')



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["brand", "model", "year", "body_type", "engine_type", "mileage", "price"]

NewListingImagesFormSet = inlineformset_factory(Listing, ListingImage, fields=['imagepath'], extra=4)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'style': 'color: gray;'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # Remove the default help text for username