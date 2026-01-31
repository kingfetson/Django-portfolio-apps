import os
import sys

# Find settings.py
settings_files = []
for root, dirs, files in os.walk('.'):
    if 'settings.py' in files:
        settings_path = os.path.join(root, 'settings.py')
        settings_files.append(settings_path)

if not settings_files:
    print("No settings.py found!")
    sys.exit(1)

settings_file = settings_files[0]
print(f"Found settings.py at: {settings_file}")

# Read current settings
with open(settings_file, 'r') as f:
    content = f.read()

# Check if CSRF settings already exist
if 'CSRF_TRUSTED_ORIGINS' not in content:
    print("Adding CSRF settings...")
    
    # Add CSRF settings at the end of the file
    csrf_settings = '''
# CSRF and Security settings for development
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
]

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# For development - remove in production
if DEBUG:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
'''
    
    with open(settings_file, 'a') as f:
        f.write(csrf_settings)
    
    print("CSRF settings added successfully!")
else:
    print("CSRF settings already exist.")

print("\n✅ CSRF fix applied!")
