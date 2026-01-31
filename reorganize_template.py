import re

with open('landing/templates/landing/index.html', 'r') as f:
    content = f.read()

# Find dishes section
dish_pattern = r'(<!-- Featured Dishes Section -->.*?{% endif %}\s*)'
dish_match = re.search(dish_pattern, content, re.DOTALL)

if dish_match:
    dishes_section = dish_match.group(1)
    
    # Remove dishes section from current location
    content = re.sub(dish_pattern, '', content, flags=re.DOTALL)
    
    # Find where to insert it (after skills section, before contact)
    # Look for: skills section closing then contact section
    insert_point = re.search(r'{% endif %}\s*\s*<section id="contact">', content, re.DOTALL)
    
    if insert_point:
        # Insert dishes before contact
        start_pos = insert_point.start()
        new_content = content[:start_pos] + dishes_section + '\n\n' + content[start_pos:]
        
        with open('landing/templates/landing/index.html', 'w') as f:
            f.write(new_content)
        print("✅ Moved dishes section before contact section")
    else:
        print("Could not find insertion point")
else:
    print("Dishes section not found")
