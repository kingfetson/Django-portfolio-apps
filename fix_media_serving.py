import os
import sys

print("=== Fixing Media File Serving ===")

# 1. Find project directory
settings_files = []
for root, dirs, files in os.walk('.'):
    if 'settings.py' in files:
        settings_path = os.path.join(root, 'settings.py')
        settings_files.append(settings_path)

if not settings_files:
    print("Error: Could not find settings.py")
    sys.exit(1)

settings_path = settings_files[0]
project_dir = os.path.dirname(settings_path)
project_name = os.path.basename(project_dir)
print(f"Project: {project_name}")
print(f"Settings: {settings_path}")

# 2. Check/update settings.py
with open(settings_path, 'r') as f:
    content = f.read()

# Ensure MEDIA settings exist
if 'MEDIA_URL' not in content:
    print("\nAdding MEDIA settings to settings.py...")
    media_settings = '''
# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
'''
    
    # Add at end of file
    with open(settings_path, 'a') as f:
        f.write(media_settings)
    print("✓ Added media settings")

# 3. Check/update urls.py
urls_path = os.path.join(project_dir, 'urls.py')
if os.path.exists(urls_path):
    with open(urls_path, 'r') as f:
        urls_content = f.read()
    
    # Check if media serving is configured
    if 'static(settings.MEDIA_URL' not in urls_content:
        print("\nUpdating urls.py for media serving...")
        
        # Import statements
        if 'from django.conf import settings' not in urls_content:
            urls_content = urls_content.replace(
                'from django.contrib import admin',
                'from django.conf import settings\nfrom django.conf.urls.static import static\nfrom django.contrib import admin'
            )
        
        # Add media serving at the end
        if 'if settings.DEBUG:' not in urls_content:
            urls_content = urls_content.rstrip() + '\n\n# Serve media files in development\nif settings.DEBUG:\n    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n'
        
        with open(urls_path, 'w') as f:
            f.write(urls_content)
        print("✓ Updated urls.py")
    else:
        print("✓ URLs already configured for media serving")
else:
    print(f"Warning: Could not find urls.py at {urls_path}")

# 4. Create media directory
media_dir = os.path.join(os.path.dirname(project_dir), 'media')
os.makedirs(media_dir, exist_ok=True)
os.makedirs(os.path.join(media_dir, 'dishes'), exist_ok=True)
print(f"\n✓ Media directory: {media_dir}")

# 5. Check current dishes
try:
    sys.path.append('.')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    
    import django
    django.setup()
    
    from dishes.models import Dish
    
    print("\n=== Current Dishes ===")
    dishes = Dish.objects.all()
    if dishes:
        for dish in dishes:
            print(f"\n{dish.name}:")
            print(f"  Category: {dish.get_category_display()}")
            print(f"  Price: ${dish.price}")
            print(f"  Has image: {bool(dish.image)}")
            if dish.image:
                print(f"  Image name: {dish.image.name}")
    else:
        print("No dishes found. Add some in the admin panel!")
        
except Exception as e:
    print(f"\nNote: Could not check dishes - {e}")

print("\n✅ Media serving fix complete!")
print("\nNext steps:")
print("1. Restart server: python manage.py runserver")
print("2. Upload dish images in admin panel")
print("3. Visit: http://localhost:8000/ to see images")
