from django.contrib import admin
from .models import Dish

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_vegetarian')
    list_filter = ('category', 'is_available', 'is_vegetarian', 'is_spicy')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'price')
        }),
        ('Details', {
            'fields': ('is_vegetarian', 'is_spicy', 'is_available', 'image')
        }),
        ('Nutritional Info', {
            'fields': ('calories', 'prep_time'),
            'classes': ('collapse',)
        }),
    )
