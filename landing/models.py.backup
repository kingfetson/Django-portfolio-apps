from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landing_portfolio')  # ADD related_name
    title = models.CharField(max_length=200, default="My Portfolio")
    tagline = models.CharField(max_length=300, default="Building amazing things with code")
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    github = models.URLField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    enable_weather_widget = models.BooleanField(default=True)
    enable_quote_widget = models.BooleanField(default=True)
    enable_github_widget = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Technology(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name



class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=300)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Skill(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50)  # Percentage
    years_of_experience = models.FloatField(default=1.0)
    short_description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    prep_time = models.IntegerField(blank=True, null=True)  # in minutes
    calories = models.IntegerField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='menu_items')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    open_in_new_tab = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title