from django.contrib import admin
from .models import Category,Listings,Comments,Bids

# Register your models here.
admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bids)