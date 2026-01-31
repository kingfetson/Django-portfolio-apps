import os

print("=== Checking menu/models.py ===")
with open('menu/models.py', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:100], 1):
        if 'class Dish' in line or '@admin.register' in line or 'DishAdmin' in line:
            print(f"Line {i}: {line.strip()}")

print("\n=== Checking menu/admin.py ===")
if os.path.exists('menu/admin.py'):
    with open('menu/admin.py', 'r') as f:
        content = f.read()
        print(f"File exists. Length: {len(content)} chars")
        if '@admin.register(Dish)' in content:
            print("Found @admin.register(Dish)")
        if 'class DishAdmin' in content:
            print("Found class DishAdmin")
else:
    print("menu/admin.py doesn't exist")

print("\n=== Checking for syntax errors ===")
import subprocess
result = subprocess.run(['python', '-m', 'py_compile', 'menu/admin.py'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print("✓ menu/admin.py has valid syntax")
else:
    print("✗ Syntax error in menu/admin.py:")
    print(result.stderr)
