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
    form = ResetPasswordForm()
    try:
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
            return render(request, 'password_reset_confirm.html', {'form':form, 'username':username})
    except Exception as error:
        showConf = True
        confirmationMessage = f'There has been an error processing your password request. {error if settings.DEBUG else ''}'
        confirmationButton = 'Back to log in page'
        confirmationTitle = 'Error occurred.'
        confirmationRedirectURL = reverse('login')
        return render(request, 'password_reset_confirm.html', {
                    'form':form,
                    'confirmationMessage': confirmationMessage,
                    'confirmationButton': confirmationButton,
                    'confirmationTitle': confirmationTitle,
                    'confirmationRedirectURL': confirmationRedirectURL,
                    'isError': True,
                    'showConf': showConf,
                    'username': username,
                })


def password_reset(request):
    try:
        form = ForgotPasswordForm()
        if request.method == 'POST':
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                return redirect(reverse('password-reset-confirm', args=[username]))
        
        return render(request, 'password_reset.html', {'form': form})
    except Exception as error:
        showConf = True
        confirmationMessage = 'There has been an error processing your password request.'
        confirmationButton = 'Back to log in page'
        confirmationTitle = f'Error occurred. {error if settings.DEBUG else ''}'
        confirmationRedirectURL = reverse('login')
        return render(request, 'password_reset.html', {
                    'form':form,
                    'confirmationMessage': confirmationMessage,
                    'confirmationButton': confirmationButton,
                    'confirmationTitle': confirmationTitle,
                    'confirmationRedirectURL': confirmationRedirectURL,
                    'isError': True,
                    'showConf': showConf,
                })

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

def custom_505(request, exception):
    return render(request, '505.html', status=500)

@login_required()
def profile(request):
    user = request.user
    confirmationConfig = {
        "showConf": False,
        "isError": False,
        "confirmationTitle": '',
        "confirmationMessage": '',
        "confirmationButton": '',
        "confirmationRedirectURL": '',
    }
    # Initialize form
    form = UserUpdateForm(instance=user)
    is_regular_user = user.groups.filter(name='RegularUsers').exists()
    is_seller = user.groups.filter(name='Sellers').exists()
    is_super_user = user.groups.filter(name='SuperUsers').exists()

    # Fetch or create the SellerUser instance if the user is a seller
    seller_user = SellerUser.objects.get_or_create(user=user)[0] if is_seller else None

    # Determine if form should be editable
    form_editable = request.POST.get('form_editable', 'false') == 'true'

    if request.method == 'POST':
        if 'edit' in request.POST:
            form_editable = True
        elif 'accept_offer' in request.POST or 'decline_offer' in request.POST:
            offer_id = request.POST.get('offer_id')
            offer = get_object_or_404(Offer, id=offer_id)

            if offer.listing.user == user:
                if 'accept_offer' in request.POST:
                    try:
                        # Update offer status to ACCEPTED
                        offer.status = Offer.ACCEPTED
                        offer.save()

                        # Update listing status to SOLD = TRUE
                        offer.listing.sold = True
                        # change Listing Price to the Accepted offer price 
                        offer.listing.price = offer.offeredPrice
                        offer.listing.save()

                        confirmationConfig.update({
                            'showConf': True,
                            'isError': False,
                            'confirmationTitle': 'Offer Accepted.',
                            'confirmationMessage': 'You have successfully accepted the offer. The payment will be processed.',
                            'confirmationButton': 'Back to My Profile',
                            'confirmationRedirectURL': '/profile'
                        })
                    except Exception as e:
                        confirmationConfig.update({
                            'showConf': True,
                            'isError': True,
                            'confirmationTitle': 'An Error has occurred.',
                            'confirmationMessage': 'Your offer decision has not been processed.',
                            'confirmationButton': 'Back to My Profile',
                            'confirmationRedirectURL': '/profile'
                        })
                elif 'decline_offer' in request.POST:
                    try:
                        # Update offer status to DECLINED
                        offer.status = Offer.DECLINED
                        offer.save()

                        # Update listing status to SOLD = FALSE
                        offer.listing.sold = False
                        offer.listing.save()

                        confirmationConfig.update({
                            'showConf': True,
                            'isError': False,
                            'confirmationTitle': 'Offer Declined.',
                            'confirmationMessage': 'You have successfully declined the offer.',
                            'confirmationButton': 'Back to My Profile',
                            'confirmationRedirectURL': '/profile'
                        })
                    except Exception as e:
                        confirmationConfig.update({
                            'showConf': True,
                            'isError': True,
                            'confirmationTitle': 'An Error has occurred.',
                            'confirmationMessage': 'Your offer decision has not been processed.',
                            'confirmationButton': 'Back to My Profile',
                            'confirmationRedirectURL': '/profile'
                        })
        else:
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                try:
                    form.save()
                    if is_seller and seller_user:
                        seller_user.company_name = request.POST.get('company_name', '')
                        seller_user.save()

                    confirmationConfig.update({
                        'showConf': True,
                        'isError': False,
                        'confirmationTitle': 'Profile Updated',
                        'confirmationMessage': 'Your profile has been updated successfully.',
                        'confirmationButton': 'Close',
                        'confirmationRedirectURL': ''
                    })
                except Exception as e:
                    confirmationConfig.update({
                        'showConf': True,
                        'isError': True,
                        'confirmationTitle': 'An Error has occurred.',
                        'confirmationMessage': 'Your profile changes have not been saved.',
                        'confirmationButton': 'Close',
                        'confirmationRedirectURL': ''
                    })
    else:
        form = UserUpdateForm(instance=user)

    # Fetch listings, orders, and offers
    if is_super_user:
        listings = Listing.objects.all()
        sellers = SellerUser.objects.all()
    else:
        listings = Listing.objects.filter(user=user)
        for listing in listings:
            if (listing.sold== True) and (listing.type == 'used'):
            # Fetch the accepted offer for the listing
                accepted_offer = Offer.objects.filter(listing=listing, status=Offer.ACCEPTED).first()

                if accepted_offer:
                    listing.price = accepted_offer.offeredPrice
                    listing.save()
    
        sellers = None

    listingsPaginator = Paginator(listings, 5)
    listings_page_number = request.GET.get("listings_page")
    listings_page_obj = listingsPaginator.get_page(listings_page_number)

    #Order History

    orders = Offer.objects.filter(user=user)
    ordersPaginator = Paginator(orders, 5)
    orders_page_number = request.GET.get("orders_page")
    orders_page_obj = ordersPaginator.get_page(orders_page_number)

    #Offers Received

    # Only show pending offers in the offers_received table

    offers = Offer.objects.filter(listing__user=user, status=Offer.PENDING)
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
        "showConf": confirmationConfig['showConf'],
        "isError": confirmationConfig['isError'],
        "confirmationMessage": confirmationConfig['confirmationMessage'],
        "confirmationTitle": confirmationConfig['confirmationTitle'],
        "confirmationButton": confirmationConfig['confirmationButton'],
        "confirmationRedirectURL": confirmationConfig['confirmationRedirectURL'],
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
        "isError": False,
        "confirmationTitle" : '',
        "confirmationMessage" : '',
        "confirmationButton" : '',
        "confirmationRedirectURL" : '',
    }
    listing = get_object_or_404(Listing, id=listingId)
    listingImages = listing.images.all()
    try:
        if request.method == 'POST':
            if('delete' in request.POST):
                # Creates copy of pk in memory to show page with modal and deleted listing information
                listingId = listing.pk
                listing.delete()
                listing.pk = listingId
                form = ListingForm(initial={'listingImages': list(listingImages.values()) }, instance=listing, disabled=request.user.is_superuser)
                confirmationConfig['showConf'] = True
                confirmationConfig['confirmationTitle'] = 'Listing removed'
                confirmationConfig['confirmationMessage'] = 'The listing was successfully delete'
                confirmationConfig['confirmationButton'] = 'Back to My Profile'
                confirmationConfig['confirmationRedirectURL'] = '/profile'
            else:
                formData = request.POST.copy()
                formData.update({ "type": listing.type })
                form = ListingForm(formData, request.FILES, instance=listing, disabled=request.user.is_superuser)
                if(form.is_valid()):
                    form.instance.user = request.user
                    form.save()
                    # print('listingImages', listingImages)
                    form = ListingForm(initial={'listingImages': list(listingImages.values()) }, instance=listing, disabled=request.user.is_superuser)
                    confirmationConfig['showConf'] = True
                    confirmationConfig['confirmationTitle'] = 'Listing updated'
                    confirmationConfig['confirmationMessage'] = 'The changes you made have been saved to your listing'
                    confirmationConfig['confirmationButton'] = 'Back to My Profile'
                    confirmationConfig['confirmationRedirectURL'] = '/profile'
                else:
                    print('form errors', form.errors)
        else:
            form = ListingForm(initial={'listingImages': list(listingImages.values()) }, instance=listing, disabled=request.user.is_superuser)

        context = { 'form': form, 'listing': listing, 'Listing': Listing } | confirmationConfig
        return render(request, 'profile/create_edit_listing.html', context=context)

    except Exception as error:
        confirmationConfig['showConf'] = True
        confirmationConfig['isError'] = True
        confirmationConfig['confirmationTitle'] = 'Error occurred'
        confirmationConfig['confirmationMessage'] = f"An error occured while {'deleting' if 'delete' in request.POST else 'updating'} your listing. Please try again later {error if settings.DEBUG else ''}"
        confirmationConfig['confirmationButton'] = 'Back to My Profile'
        confirmationConfig['confirmationRedirectURL'] = '/profile'
        form = ListingForm(initial={'listingImages': list(listingImages.values()) }, instance=listing, disabled=request.user.is_superuser)
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
                    userToUpdate.first_name = form.cleaned_data['first_name']
                    userToUpdate.last_name = form.cleaned_data['last_name']
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
                'first_name': seller.user.first_name,
                'last_name': seller.user.last_name ,
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

from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Listing, Offer
from .forms import PaymentForm, OfferForm


@csrf_protect
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user = request.user
    confirmationConfig = {
        "showConf": False,
        "confirmationTitle": '',
        "confirmationMessage": '',
        "confirmationButton": '',
        "confirmationRedirectURL": '',
        "isError": False
    }
    form = PaymentForm()
    offer_form = OfferForm()

    if request.user == listing.user:
        messages.error(request, "You cannot make an offer on your own listing.")
        return render(request, 'listing_detail.html', context={
            'listing': listing,
            'form': form,
            'offer_form': offer_form
        } | confirmationConfig)

    if request.method == 'POST':
        if 'payment_submit' in request.POST:
            try:
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
                            'confirmationRedirectURL': '/profile',
                            'isError': False
                        })

                    else:
                        confirmationConfig.update({
                            'showConf': True,
                            'confirmationTitle': 'Insufficient Funds',
                            'confirmationMessage': 'You do not have enough credits in your account balance to purchase this vehicle.',
                            'confirmationButton': 'Back to Catalog',
                            'confirmationRedirectURL': '/catalog',
                            'isError': False
                        })

            except Exception as e:
                # Log the exception if needed
                confirmationConfig.update({
                    'showConf': True,
                    'confirmationTitle': 'An Error Occurred',
                    'confirmationMessage': f'An unexpected error occurred during payment: {str(e)}',
                    'confirmationButton': 'Back to Listing',
                    'confirmationRedirectURL': f'/catalog/listing/{listing_id}/',
                    'isError': True
                })

        elif 'offer_submit' in request.POST:
            try:
                offer_form = OfferForm(request.POST)
                if offer_form.is_valid():
                    offered_price = offer_form.cleaned_data['offeredPrice']

                    Offer.objects.create(user=user, listing=listing, offeredPrice=offered_price, status='pending')

                    confirmationConfig.update({
                        'showConf': True,
                        'confirmationTitle': 'Offer Sent',
                        'confirmationMessage': 'Your offer has been submitted. You can view your pending offers in your Order History.',
                        'confirmationButton': 'Back to My Profile',
                        'confirmationRedirectURL': '/profile',
                        'isError': False
                    })


            except Exception as e:
                # Log the exception if needed
                confirmationConfig.update({
                    'showConf': True,
                    'confirmationTitle': 'An Error Occurred',
                    'confirmationMessage': f'An unexpected error occurred during offer submission: {str(e)}',
                    'confirmationButton': 'Back to Listing',
                    'confirmationRedirectURL': f'/catalog/listing/{listing_id}/',
                    'isError': True
                })

    context = {
        'listing': listing,
        'form': form,
        'offer_form': offer_form,
    } | confirmationConfig

    return render(request, 'listing_detail.html', context=context)
