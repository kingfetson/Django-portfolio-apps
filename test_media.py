import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_framework.settings')
django.setup()

from django.conf import settings
from dishes.models import Dish

print("=== Media Configuration Test ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_ROOT exists: {os.path.exists(settings.MEDIA_ROOT)}")

print("\n=== Dish Images ===")
for dish in Dish.objects.all():
    print(f"\n{dish.name}:")
    if dish.image:
        print(f"  Image field: {dish.image}")
        print(f"  Image URL: {dish.image.url}")
        print(f"  Image path: {dish.image.path}")
        print(f"  File exists: {os.path.exists(dish.image.path)}")
        
        # Test full URL
        full_url = f"http://localhost:8000{dish.image.url}"
        print(f"  Full URL: {full_url}")
    else:
        print(f"  No image uploaded")
