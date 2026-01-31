import os
import sys

# Add project to path
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_framework.settings')

import django
django.setup()

from django.conf import settings

print("=== Media Configuration Check ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")

# Check if directories exist
print("\n=== Directory Check ===")
dirs_to_check = [
    settings.MEDIA_ROOT,
    os.path.join(settings.MEDIA_ROOT, 'dishes'),
    settings.STATIC_ROOT if hasattr(settings, 'STATIC_ROOT') else 'Not set',
]

for directory in dirs_to_check:
    if directory and os.path.exists(directory):
        print(f"✓ {directory} exists")
    else:
        print(f"✗ {directory} does not exist")

# Check dishes with images
from dishes.models import Dish
print("\n=== Dishes with Images ===")
dishes = Dish.objects.all()
if dishes:
    for dish in dishes:
        if dish.image:
            print(f"✓ {dish.name}: Has image - {dish.image.url}")
            print(f"  Image path: {dish.image.path}")
            print(f"  File exists: {os.path.exists(dish.image.path)}")
        else:
            print(f"✗ {dish.name}: No image uploaded")
else:
    print("No dishes found in database")
