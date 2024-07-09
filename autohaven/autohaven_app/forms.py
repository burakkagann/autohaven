from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.forms import inlineformset_factory
from .models import Listing, ListingImage ,Seller

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email')



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class NewListingForm(forms.ModelForm):
    newImages = MultipleFileField(required=False)
    class Meta:
        model = Listing
        fields = ["brand", "model", "description", "year", "body_type", "engine_type", "mileage", "price"]
    
    def save(self):
        newListing = super(NewListingForm, self).save()
        print('newListing', newListing)
        files = self.cleaned_data['newImages']
        print('files', files)
        for f in files:
            print('file', f)
            newListingImage = ListingImage(listing=newListing, imagepath=f)
            newListingImage.save()
            
    

ListingImagesFormSet = inlineformset_factory(Listing, ListingImage, fields=['imagepath'], extra=4)

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


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['company_name', 'email_address', 'username']
        labels = {
            'company_name': 'Company name',
            'email_address': 'Email address',
            'username': 'Username',
        }
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Company name'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }        