from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User, Group
from datetime import datetime
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Listing, ListingImage, SellerUser,Offer

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
    listingImages = MultipleFileField(required=False)
    class Meta:
        model = Listing
        fields = [ "title", "brand", "model", "description", "year", "body_type", "engine_type", "mileage", "price", "type"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['mileage'].required = False

    def save(self):
        newListing = super(NewListingForm, self).save()
        print('newListing', newListing)
        files = self.cleaned_data['listingImages']
        print('files', files)
        for f in files:
            print('file', f)
            newListingImage = ListingImage(listing=newListing, imagepath=f)
            newListingImage.save()
        newListing.refresh_from_db()
        return newListing

class ListingForm(forms.ModelForm):
    listingImages = MultipleFileField(required=False)
    imagesToDelete = forms.ModelMultipleChoiceField(ListingImage.objects.all(), required=False)
    class Meta:
        model = Listing
        fields = [ "title", "brand", "model", "description", "year", "body_type", "engine_type", "mileage", "price", "type"]
    
    def __init__(self, *args, **kwargs):
        disabled = False
        if('disabled' in kwargs):
            disabled = kwargs['disabled']
            del kwargs['disabled']
        super().__init__(*args, **kwargs)
        if(disabled):
            for field in self.fields.values():
                field.disabled = True
        if kwargs['instance'] is not None:
            querySetImagesToDelete = ListingImage.objects.filter(listing=kwargs['instance'])
            self.fields['imagesToDelete'].queryset = querySetImagesToDelete
        

    def save(self):
        listing = super(ListingForm, self).save()
        files = self.cleaned_data['listingImages']
        for f in files:
            listingImage = ListingImage(listing=listing, imagepath=f)
            listingImage.save()
        
        imagesToDelete = self.cleaned_data['imagesToDelete']
        ListingImage.objects.filter(id__in=imagesToDelete).delete()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # Remove the default help text for username



class CreateSellerForm(forms.Form):
    username = UsernameField(label='Username')
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email')
    company_name = forms.CharField(label='Company Name', max_length=100)
    

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (User.objects.filter(username__iexact=username).exists()):
            raise ValidationError("User with this username already exists.")
        return username

    def save(self):
        newUser = User(username = self.cleaned_data['username'],
                        email = self.cleaned_data['email'], 
                        first_name=self.cleaned_data['first_name'],
                        last_name=self.cleaned_data['last_name'])
        newUser.save()
        newUser.groups.add(Group.objects.get(name='Sellers'))
        newSellerUser = SellerUser(user = newUser,company_name = self.cleaned_data['company_name'])
        newSellerUser.save()
        return newUser

class UpdateSellerForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'color: gray;'})
    )
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email')
    company_name = forms.CharField(label='Company Name', max_length=100)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username__iexact=username).exists():
            raise ValidationError("User with this username doesn't exist")
        return username

    def save(self, commit=True):
        userToUpdate = User.objects.get(username=self.cleaned_data['username'])
        userToUpdate.first_name = self.cleaned_data['first_name']
        userToUpdate.last_name = self.cleaned_data['last_name']
        userToUpdate.email = self.cleaned_data['email']
        userToUpdate.selleruser.company_name = self.cleaned_data['company_name']
        if commit:
            userToUpdate.save()
            userToUpdate.selleruser.save()
        return userToUpdate
    
        
class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
class PaymentForm(forms.Form):
    account_balance = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offeredPrice']
        labels = {
            'offeredPrice': '',
        }
        widgets = {
            'offeredPrice': forms.TextInput(attrs={'class': 'form-control'}),
        }

    