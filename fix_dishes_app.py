import os
import sys
import subprocess

print("=== Fixing Dishes App Configuration ===")

# 1. Check if dishes app exists
if not os.path.exists('dishes'):
    print("Creating dishes app...")
    subprocess.run(['python', 'manage.py', 'startapp', 'dishes'], check=True)

# 2. Create necessary files if they don't exist
files_to_create = {
    'dishes/apps.py': '''from django.apps import AppConfig

class DishesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dishes'
    verbose_name = 'Dishes Menu'
''',
    'dishes/models.py': '''from django.db import models

class Dish(models.Model):
    CATEGORIES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
        ('special', 'Special'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    calories = models.IntegerField(blank=True, null=True)
    prep_time = models.IntegerField(help_text="Preparation time in minutes", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = 'Dishes'
    
    def __str__(self):
        return f"{self.name} (${self.price})"
''',
    'dishes/admin.py': '''from django.contrib import admin
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
'''
}

for filepath, content in files_to_create.items():
    if not os.path.exists(filepath):
        print(f"Creating {filepath}...")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)

# 3. Add to INSTALLED_APPS
print("\nAdding 'dishes' to INSTALLED_APPS...")
# Find settings.py
settings_files = [f for f in os.listdir('.') if f == 'settings.py']
if not settings_files:
    # Look in subdirectories
    for root, dirs, files in os.walk('.'):
        if 'settings.py' in files:
            settings_path = os.path.join(root, 'settings.py')
            break

if settings_path:
    with open(settings_path, 'r') as f:
        content = f.read()
    
    if "'dishes'" not in content:
        # Find where to insert (after 'skills')
        if "'skills'" in content:
            new_content = content.replace("'skills',", "'skills',\n    'dishes',")
            with open(settings_path, 'w') as f:
                f.write(new_content)
            print(f"Added 'dishes' to INSTALLED_APPS in {settings_path}")
        else:
            print("Could not find 'skills' in INSTALLED_APPS. Please add 'dishes' manually.")
    else:
        print("'dishes' already in INSTALLED_APPS")

print("\n✅ Fix applied! Now run migrations:")
print("python manage.py makemigrations dishes")
print("python manage.py migrate dishes")
