from django.contrib import admin
from .models import Listing, Offer, ListingImage


# 
class ListingImageInline(admin.StackedInline):
    model = ListingImage
    extra = 3


class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]


# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Offer)