from django.db import models

class MenuItem(models.Model):
    MENU_TYPES = [
        ('header', 'Header Menu'),
        ('footer', 'Footer Menu'),
        ('social', 'Social Menu'),
    ]
    
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                              null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    icon_class = models.CharField(max_length=50, blank=True)
    open_in_new_tab = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['menu_type', 'order', 'title']
    
    def __str__(self):
        return f"{self.get_menu_type_display()}: {self.title}"

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
    is_available = models.BooleanField(default=True)  # Changed from 'available' to 'is_available'
    
    # Optional: Nutritional info
    calories = models.IntegerField(blank=True, null=True)
    prep_time = models.IntegerField(help_text="Preparation time in minutes", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = 'Dishes'
    
    def __str__(self):
        return f"{self.name} (${self.price})"
