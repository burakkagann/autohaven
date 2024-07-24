from django.contrib.auth.decorators import login_required ,user_passes_test
from django.shortcuts import render, redirect , get_object_or_404
from . import models
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from .models import Listing, Offer, SellerUser , User
from .forms import ForgotPasswordForm, ResetPasswordForm, SignUpForm, NewListingForm, UserUpdateForm , CreateSellerForm, UpdateSellerForm, ListingForm, PaymentForm,OfferForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import Group
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

# import logging
# logger = logging.getLogger(__name__)  # Create a logger instance

def root(request):
    return redirect('home/')

def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'login.html')

def landing_page(request):
    return render(request, 'landing_page.html')


def password_reset_confirm(request,username):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            showConf = True
            confirmationMessage = 'You successfully reset your password! You can now use this to log into your account.'
            confirmationButton = 'Back to log in page'
            confirmationTitle = 'Password changed.'
            confirmationRedirectURL = reverse('login')
            return render(request, 'password_reset_confirm.html',
                           {'form':form,
                            'confirmationMessage': confirmationMessage,
                            'confirmationButton': confirmationButton,
                            'confirmationTitle': confirmationTitle,
                            'confirmationRedirectURL': confirmationRedirectURL,
                            'showConf': showConf,
                            'username': username})
        return render(request, 'password_reset_confirm.html', {'form':form, 'username':username})
    else:
        form = ResetPasswordForm()
        return render(request, 'password_reset_confirm.html', {'form':form, 'username':username})


def password_reset(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            return redirect(reverse('password-reset-confirm', args=[username]))
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'password_reset.html', {'form': form})

def catalog_page(request):
    # Pull Listing from models (databse)
    
    #only show available cars in the catalog
    listing = models.Listing.objects.filter(sold=False)

    # Filter Listings
    brand_filter = request.GET.get('brand')
    model_filter = request.GET.get('model')
    year_filter = request.GET.get('year')
    body_type_filter = request.GET.get('body_type')
    engine_type_filter = request.GET.get('engine_type')
    mileage_filter = request.GET.get('mileage')
    price_filter = request.GET.get('price')
    offering_type_filter = request.GET.get('offering_type')

    # Apply filters
    if brand_filter:
        listing = listing.filter(brand=brand_filter)

    if model_filter:
        listing = listing.filter(model=model_filter)

    if year_filter:
        listing = listing.filter(year__lte=year_filter)

    if body_type_filter:
        listing = listing.filter(body_type=body_type_filter)

    if engine_type_filter:
        listing = listing.filter(engine_type=engine_type_filter)

    if mileage_filter:
        listing = listing.filter(mileage__lte=mileage_filter)

    if price_filter:
        listing = listing.filter(price__lte=price_filter)

    if offering_type_filter:
        listing = listing.filter(type=offering_type_filter)

    # Match  filtered listings to according images
    listing_with_images = []
    for item in listing:
        images = models.ListingImage.objects.filter(listing=item)
        first_image = images.first()
        listing_with_images.append({
            'listing': item,
            'image': first_image
        })

    # Get Filter Value Fields
    brand = models.Listing.objects.values('brand').distinct()
    model = models.Listing.objects.values('model').distinct()
    year = models.Listing.objects.values('year').distinct()
    body_type = models.Listing.objects.values('body_type').distinct()
    engine_type = models.Listing.objects.values('engine_type').distinct()

    # Display message if no listings match filters
    if len(listing_with_images) == 0:
        no_results_message = True
    else:
        no_results_message = False


    return render(request, 'catalog.html', {
        'listing': listing_with_images,
        'brand': brand,
        'model': model,
        'year': year,
        'body_type': body_type,
        'engine_type': engine_type,
        'no_results_message': no_results_message})


def register(request):
    
    showConf = False
    confirmationTitle = ""
    confirmationMessage = ""
    confirmationButton = ""
    confirmationRedirectURL = ""
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            
            regularuser_group = Group.objects.get(name='RegularUsers')
            user.groups.add(regularuser_group)
            
            showConf = True
            confirmationTitle = "Your account is complete"
            confirmationMessage = "You successfully created an account"
            confirmationButton = "Go to Login"
            confirmationRedirectURL = reverse('login')
            
        else:
            print(form.errors)
    else:
        form = SignUpForm()
        
    # If the form is invalid, render the form with errors
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append(f"{error}")

    return render(request, 'signup.html', {
        'form': form,
        'error_messages': error_messages,
        'showConf': showConf,
        'confirmationTitle': confirmationTitle,
        'confirmationMessage': confirmationMessage,
        'confirmationButton': confirmationButton,
        'confirmationRedirectURL': confirmationRedirectURL,
    })

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required()
def profile(request):
    user = request.user

    # Popup Params
    showConf = False
    isError = False
    confirmationTitle = ""
    confirmationMessage = ""
    confirmationButton = ""
    
    is_regular_user = user.groups.filter(name='RegularUsers').exists()
    is_seller = user.groups.filter(name='Sellers').exists()
    is_super_user = user.groups.filter(name='SuperUsers').exists()

    # Fetch or create the SellerUser instance if the user is a seller
    seller_user = SellerUser.objects.get_or_create(user=user)[0] if is_seller else None

    # Determine if form should be editable
    form_editable = request.POST.get('form_editable', 'false') == 'true'

    form = UserUpdateForm(instance=user)

    # Try / Except block to handle form submission Errors
    try:

        # Debug Exception
        # raise Exception('This is a testing testing error')

        if request.method == 'POST' and 'edit' in request.POST:
            form_editable = True
        elif request.method == 'POST':
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                if is_seller and seller_user:
                    seller_user.company_name = request.POST.get('company_name', '')
                    seller_user.save()

                # Set Popup Params     
                showConf = True
                confirmationTitle = "Profile Updated"
                confirmationMessage = "Your profile is updated succesfully"
                confirmationButton = "Close"
                
        else:
            form = UserUpdateForm(instance=user)

    except Exception as e:
        showConf = True
        isError = True
        confirmationTitle = "An Error has occured!"
        confirmationMessage = "Changes have not been saved. \n Error: " + e.__str__()
        confirmationButton = "Close"

               
        

    # Listings
       
    if is_super_user:
        listings = Listing.objects.all()
        sellers = SellerUser.objects.all()
    else:
        listings = Listing.objects.filter(user=user) 
        sellers = None
    
    #listings = Listing.objects.all() #this can be used to test listing table instead of above if statement

    listingsPaginator = Paginator(listings, 5)  # Show 10 listings per page.

    listings_page_number = request.GET.get("listings_page")
    listings_page_obj = listingsPaginator.get_page(listings_page_number)

    #Orders
    orders = Offer.objects.filter(user=user)
    ordersPaginator = Paginator(orders, 5)
    orders_page_number = request.GET.get("orders_page")
    orders_page_obj = ordersPaginator.get_page(orders_page_number)

    # Offers received
    offers = Offer.objects.filter(user=user)
    offersPaginator = Paginator(offers, 5)
    offers_page_number = request.GET.get("offers_page")
    offers_page_obj = offersPaginator.get_page(offers_page_number)

    context = {
        'form': form,
        'user': user,
        'seller_user': seller_user,
        'is_regular_user': is_regular_user,
        'is_seller': is_seller,
        'is_super_user': is_super_user,
        'listings_page_obj': listings_page_obj,
        'offers_page_obj': offers_page_obj,
        'orders_page_obj': orders_page_obj,
        'sellers': sellers,
        "showConf": showConf,
        "isError": isError,
        "confirmationMessage": confirmationMessage,
        "confirmationTitle": confirmationTitle,
        "confirmationButton": confirmationButton,
        "form_editable": form_editable
    }

    return render(request, 'profile/index.html', context)


        

#User Authentication Views 

def login_user(request):
    if request.method == 'POST':
        print('LOGIN VIEW POST')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('user', user)
        if user is not None:
            auth_login(request,user)
            #superuser
            if request.user.groups.filter(name='RegularUsers').exists():
                return redirect('home')

            elif user.is_superuser:
                
                return redirect('profile')
            #seller
            elif request.user.groups.filter(name='Sellers').exists():

                return redirect('profile')
            
            else:
                return redirect('home')
            
        else:
            print('Error login')
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'login.html', {'error': error_message})
            
        
    return render(request, 'login.html')

@login_required()
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def logout_view(request):
        logout(request)
        return redirect('home')

@login_required()
def new_listing(request):
    listingType = { "type": Listing.NEW if request.user.groups.filter(name='Sellers').exists() else Listing.USED }
    confirmationConfig = {
        "showConf" : False,
        "isError"  : False,
        "confirmationTitle" : '',
        "confirmationMessage" : '',
        "confirmationButton" : '',
        "confirmationRedirectURL" : '',
    }
    try:
        if request.method == 'POST':
            formData = request.POST.copy()
            formData.update(listingType)
            form = NewListingForm(formData, request.FILES)

            if form.is_valid():
                form.instance.user = request.user
                listing = form.save()
                confirmationConfig['showConf'] = True
                confirmationConfig['confirmationTitle'] = 'New listing uploaded'
                confirmationConfig['confirmationMessage'] = 'Your listing has been successfully added to the catalog. You will receive a confirmation email shortly regarding your upload. You can view and edit this listing in the My Listings section'
                confirmationConfig['confirmationButton'] = 'Back to My Profile'
                confirmationConfig['confirmationRedirectURL'] = '/profile'
                listingImages = listing.images.all()
                form = ListingForm(initial={'listingImages': list(listingImages.values())}, instance=listing)
            else:
                print('form errors', form.errors)
        else:
            formData = listingType
            form = NewListingForm(initial=listingType)
    except Exception as e:
        confirmationConfig['showConf'] = True
        confirmationConfig['isError'] = True
        confirmationConfig['confirmationTitle'] = "An Error has occurred!"
        confirmationConfig['confirmationMessage'] = "Your listing could not be created."
        if settings.DEBUG:
            confirmationConfig['confirmationMessage'] += "\n Error: " + str(e)
        confirmationConfig['confirmationButton'] = "Close"
        form = NewListingForm(initial=listingType)
        
    context = { 
        'form': form,
        'Listing': Listing,
    } | confirmationConfig
    return render(request, 'profile/create_edit_listing.html', context=context)

@login_required()
def manage_listing(request, listingId):
    confirmationConfig = {
        "showConf" : False,
        "confirmationTitle" : '',
        "confirmationMessage" : '',
        "confirmationButton" : '',
        "confirmationRedirectURL" : '',
    }
    listing = get_object_or_404(Listing, id=listingId)
    if request.method == 'POST':
        listingImages = listing.images.all()
        if(listing):
            if('delete' in request.POST):
                # Creates copy of pk in memory to show page with modal and deleted listing information
                listingId = listing.pk
                listing.delete()
                listing.pk = listingId
                form = ListingForm(initial={'listingImages': list(listingImages.values()) }, instance=listing)
                confirmationConfig['showConf'] = True
                confirmationConfig['confirmationTitle'] = 'Listing removed'
                confirmationConfig['confirmationMessage'] = 'The listing was successfully delete'
                confirmationConfig['confirmationButton'] = 'Back to My Profile'
                confirmationConfig['confirmationRedirectURL'] = '/profile'
            else:
                formData = request.POST.copy()
                formData.update({ "type": listing.type })
                form = ListingForm(formData, request.FILES, instance=listing)
                if(form.is_valid()):
                    form.instance.user = request.user
                    form.save()
                    # print('listingImages', listingImages)
                    form = ListingForm(initial={'listingImages': list(listingImages.values()) }, instance=listing)
                    confirmationConfig['showConf'] = True
                    confirmationConfig['confirmationTitle'] = 'Listing updated'
                    confirmationConfig['confirmationMessage'] = 'The changes you made have been saved to your listing'
                    confirmationConfig['confirmationButton'] = 'Back to My Profile'
                    confirmationConfig['confirmationRedirectURL'] = '/profile'
                else:
                    print('form errors', form.errors)
    else:
        listingImages = listing.images.all()
        form = ListingForm(initial={'listingImages': list(listingImages.values()) }, instance=listing)

    context = { 'form': form, 'listing': listing, 'Listing': Listing } | confirmationConfig
    return render(request, 'profile/create_edit_listing.html', context=context)


def seller_list(request):
    sellers = SellerUser.objects.all()
    return render(request, 'profile/sellers.html', {'sellers': sellers})

def manage_seller(request, id):
    seller = get_object_or_404(SellerUser, id=id)
    confirmationConfig = {
        "showConf" : False,
        "isError"  : False,
        "confirmationTitle" : '',
        "confirmationMessage" : '',
        "confirmationButton" : '',
        "confirmationRedirectURL" : '',
    }
    
    try:
        if request.method == 'POST':
            if 'delete' in request.POST:
                seller.user.delete()
                return redirect('/profile/')
            else:
                form = UpdateSellerForm(request.POST)
                if form.is_valid():
                    userToUpdate = User.objects.get(username=seller.user.username)
                    userToUpdate.email = form.cleaned_data['email']
                    seller.company_name = form.cleaned_data['company_name']
                    userToUpdate.save()
                    seller.save()
                    confirmationConfig["showConf"] = True
                    confirmationConfig["confirmationTitle"] = 'Changes saved.'
                    confirmationConfig["confirmationMessage"] = 'The changes you made have been saved to the seller profile!'
                    confirmationConfig["confirmationButton"] =  'Back to My Profile'
                    confirmationConfig["confirmationRedirectURL"] = reverse('profile')
        else:
            form = UpdateSellerForm(initial={
                'username': seller.user.username,
                'email': seller.user.email,
                'company_name': seller.company_name,
            })
            
    except Exception as e:
        confirmationConfig['showConf'] = True
        confirmationConfig['isError'] = True
        confirmationConfig['confirmationTitle'] = "An Error has occurred!"
        confirmationConfig['confirmationMessage'] = "There was an error updating the seller information."
        if settings.DEBUG:
            confirmationConfig['confirmationMessage'] += "\n Error: " + str(e)
        confirmationConfig['confirmationButton'] = "Close"
        form = UpdateSellerForm(initial={
            'username': seller.user.username,
            'first_name': seller.user.first_name,
            'last_name': seller.user.last_name ,
            'email': seller.user.email,
            'company_name': seller.company_name,
        })   
    context = {'form': form, 'seller': seller } | confirmationConfig
    return render(request, 'profile/manage_seller.html', context)

def upload_new_seller(request):
    confirmationConfig = {
        "showConf" : False,
        "isError"  : False,
        "confirmationTitle" : '',
        "confirmationMessage" : '',
        "confirmationButton" : '',
        "confirmationRedirectURL" : '',
    }
    try :
        
        if request.method == 'POST':
            form = CreateSellerForm(request.POST)
            if form.is_valid():
                form.save()
                confirmationConfig["showConf"] = True
                confirmationConfig["confirmationTitle"] = 'New seller created'
                confirmationConfig["confirmationMessage"] = 'The seller will receive an email with their login details and further information on how to get started and create their own password. You will receive a confirmation message shortly about your upload.'
                confirmationConfig["confirmationButton"] =  'Back to My Profile'
                confirmationConfig["confirmationRedirectURL"] = reverse('profile')
            else:
                # Collect form errors into a single message , this for django filed error 
                error_messages = " ".join([f"{field}: {error}" for field, errors in form.errors.items() for error in errors])
                confirmationConfig["showConf"] = True
                confirmationConfig["isError"] = True
                confirmationConfig["confirmationTitle"] = "Error"
                confirmationConfig["confirmationMessage"] = f"There were errors in the form submission: {error_messages} \n Changes have not been saved."
                confirmationConfig["confirmationButton"] = "Close"    
        else:
            form = CreateSellerForm()
        context = { 'form': form } | confirmationConfig
        return render(request, 'profile/upload_new_seller.html', context)
    
    except Exception as e:
        #this for ganaral errors 
        confirmationConfig["showConf"] = True
        confirmationConfig["isError"]  = True
        confirmationConfig["confirmationTitle"] = "An Error has occured!"
        confirmationConfig["confirmationMessage"] = "Changes have not been saved. \n Error: " + e.__str__()
        confirmationConfig["confirmationButton"] = "Close"
        return render(request, 'profile/upload_new_seller.html', {'form': form} | confirmationConfig)

@csrf_protect
def listing_detail(request,listing_id):
    listing = get_object_or_404(Listing,pk=listing_id)
    user = request.user
    confirmationConfig = {
            "showConf": False,
            "confirmationTitle": '',
            "confirmationMessage": '',
            "confirmationButton": '',
            "confirmationRedirectURL": '',
        }
    form = PaymentForm()
    offer_form = OfferForm()
    
    if request.user == listing.user:
        messages.error(request, "You cannot make an offer on your own listing.")

    if request.method == 'POST':
        if 'payment_submit' in request.POST:  
            form = PaymentForm(request.POST)
            if form.is_valid():
                account_balance = form.cleaned_data['account_balance']
                if account_balance >= listing.price:
                    listing.sold = True
                    listing.save()
                    Offer.objects.create(user=user, listing=listing, offeredPrice=listing.price, status='accepted')

                    confirmationConfig.update({
                        'showConf': True,
                        'confirmationTitle': 'Payment Successful',
                        'confirmationMessage': 'You successfully purchased this listing. The payment will be reflected under the Order History section in your profile.',
                        'confirmationButton': 'Back to My Profile',
                        'confirmationRedirectURL': '/profile'
                    })

                else:
                    confirmationConfig.update({
                        'showConf': True,
                        'confirmationTitle': 'Insufficient Funds',
                        'confirmationMessage': 'You do not have enough credits in your account balance to purchase this vehicle.',
                        'confirmationButton': 'Back to Catalog',
                        'confirmationRedirectURL': '/catalog'
                    })
                    
        elif 'offer_submit' in request.POST: # Handle offer form
            offer_form = OfferForm(request.POST)
            if offer_form.is_valid():
                offered_price = offer_form.cleaned_data['offeredPrice']

                Offer.objects.create(user=user, listing=listing, offeredPrice=offered_price, status='pending')

                confirmationConfig.update({
                    'showConf': True,
                    'confirmationTitle': 'Offer Sent',
                    'confirmationMessage': 'Your offer has been submitted. You can view your pending offers in your profile.',
                    'confirmationButton': 'Back to My Profile',
                    'confirmationRedirectURL': '/profile'
                })

        else:
                messages.error(request, 'Invalid form submission. Please use the payment or offer form.')

    context = {
        'listing': listing,
        'form': form,
        'offer_form': offer_form,
    } | confirmationConfig

    return render(request, 'listing_detail.html', context=context)

