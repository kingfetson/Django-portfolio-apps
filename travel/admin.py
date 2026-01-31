from django.contrib import admin
from .models import Destination, Trip, TravelPhoto, TravelTip, TravelWishlist

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'continent', 'estimated_cost']
    list_filter = ['continent', 'country']
    search_fields = ['name', 'country', 'description']
    prepopulated_fields = {'slug': ('name', 'country')}

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'trip_type', 'duration_days', 'price', 'featured']
    list_filter = ['trip_type', 'featured', 'destination']
    search_fields = ['title', 'description', 'highlights']
    prepopulated_fields = {'slug': ('title',)}
    
class TravelPhotoInline(admin.TabularInline):
    model = TravelPhoto
    extra = 1

@admin.register(TravelPhoto)
class TravelPhotoAdmin(admin.ModelAdmin):
    list_display = ['trip', 'caption', 'uploaded_at']
    list_filter = ['trip']

@admin.register(TravelTip)
class TravelTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'featured', 'created_at']
    list_filter = ['category', 'featured']
    search_fields = ['title', 'content']

@admin.register(TravelWishlist)
class TravelWishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'destination', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'destination__name', 'notes']
