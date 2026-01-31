import os
import re

# Find where Dish model is
dish_location = None
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('models.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                if 'class Dish' in f.read():
                    dish_location = filepath
                    break
    if dish_location:
        break

print(f"Dish model found in: {dish_location}")

# Determine app name
if 'dishes/models.py' in dish_location:
    app_name = 'dishes'
    admin_file = 'dishes/admin.py'
    import_statement = 'from dishes.models import Dish'
elif 'menu/models.py' in dish_location:
    app_name = 'menu'
    admin_file = 'menu/admin.py'
    import_statement = 'from menu.models import Dish'
else:
    print("Could not determine app name from path")
    exit(1)

print(f"Dish is in app: {app_name}")
print(f"Admin file should be: {admin_file}")

# Fix menu/admin.py if DishAdmin is there
menu_admin_path = 'menu/admin.py'
if os.path.exists(menu_admin_path):
    with open(menu_admin_path, 'r') as f:
        content = f.read()
    
    if 'class DishAdmin' in content:
        print("Found DishAdmin in menu/admin.py")
        
        # Remove DishAdmin from menu/admin.py
        # Keep only MenuItemAdmin if it exists
        lines = content.split('\n')
        new_lines = []
        in_dish_admin = False
        
        for line in lines:
            if line.strip().startswith('@admin.register(Dish)') or line.strip().startswith('class DishAdmin'):
                in_dish_admin = True
                continue
            elif in_dish_admin and line.strip().startswith('class '):
                in_dish_admin = False
                new_lines.append(line)
            elif not in_dish_admin:
                new_lines.append(line)
        
        # Remove import if it exists
        new_content = '\n'.join(new_lines)
        new_content = re.sub(r'from \S+ import Dish\n', '', new_content)
        new_content = re.sub(r'import Dish\n', '', new_content)
        
        with open(menu_admin_path, 'w') as f:
            f.write(new_content)
        
        print("Removed DishAdmin from menu/admin.py")
        
        # Create/update dishes/admin.py or menu/admin.py
        admin_content = f'''from django.contrib import admin
{import_statement}

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_vegetarian')
    list_filter = ('category', 'is_available', 'is_vegetarian', 'is_spicy')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    
    fieldsets = (
        ('Basic Info', {{
            'fields': ('name', 'category', 'description', 'price')
        }}),
        ('Details', {{
            'fields': ('is_vegetarian', 'is_spicy', 'is_available', 'image')
        }}),
        ('Nutritional Info', {{
            'fields': ('calories', 'prep_time'),
            'classes': ('collapse',)
        }}),
    )
'''
        
        # Ensure admin file exists
        os.makedirs(os.path.dirname(admin_file), exist_ok=True)
        
        with open(admin_file, 'w') as f:
            f.write(admin_content)
        
        print(f"Created {admin_file} with correct DishAdmin")
    else:
        print("DishAdmin not found in menu/admin.py")
else:
    print("menu/admin.py does not exist")

print("\n✅ Fix applied!")
