from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Listing, Offer, ListingImage, SellerUser


# 
class ListingImageInline(admin.StackedInline):
    model = ListingImage
    extra = 3


class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]

class SellerInline(admin.StackedInline):
    model = SellerUser
    can_delete = False
    verbose_name_plural = "Seller"


# Define a new User admin
class UserAdmin(BaseUserAdmin):

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)

        if obj is not None and obj.groups.filter(name='Sellers').exists():
            print('GONORREA')
            inline_instances.append(SellerInline(self.model, self.admin_site))

        return inline_instances


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Offer)