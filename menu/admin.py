from django.contrib import admin
from .models import MenuItem, Dish  # Make sure Dish is imported

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu_type', 'url', 'order', 'is_active', 'parent')
    list_filter = ('menu_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'url')
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'url', 'menu_type', 'parent')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'icon_class', 'open_in_new_tab')
        }),
    )

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
