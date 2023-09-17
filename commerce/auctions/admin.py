from django.contrib import admin

# Register your models here.

from .models import Listings

admin.site.register(Listings)
