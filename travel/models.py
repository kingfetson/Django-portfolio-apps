from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Destination(models.Model):
    CONTINENT_CHOICES = [
        ('africa', 'Africa'),
        ('asia', 'Asia'),
        ('europe', 'Europe'),
        ('north_america', 'North America'),
        ('south_america', 'South America'),
        ('oceania', 'Oceania'),
        ('antarctica', 'Antarctica'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=50, choices=CONTINENT_CHOICES)
    description = models.TextField()
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Estimated cost per person in USD")
    featured_image = models.ImageField(upload_to='travel/destinations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.country}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}, {self.country}"

class Trip(models.Model):
    TRIP_TYPE_CHOICES = [
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('beach', 'Beach'),
        ('honeymoon', 'Honeymoon'),
        ('family', 'Family'),
        ('solo', 'Solo'),
        ('business', 'Business'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='trips')
    trip_type = models.CharField(max_length=50, choices=TRIP_TYPE_CHOICES)
    duration_days = models.IntegerField(help_text="Duration in days")
    description = models.TextField()
    highlights = models.TextField(help_text="List trip highlights, one per line")
    itinerary = models.TextField(help_text="Detailed day-by-day itinerary")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class TravelPhoto(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='travel/photos/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.trip.title}"

class TravelTip(models.Model):
    CATEGORY_CHOICES = [
        ('packing', 'Packing'),
        ('budget', 'Budget'),
        ('safety', 'Safety'),
        ('transport', 'Transport'),
        ('accommodation', 'Accommodation'),
        ('food', 'Food'),
        ('culture', 'Culture'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    useful_links = models.TextField(blank=True, help_text="Useful links, one per line")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class TravelWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_wishlist')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Why you want to visit")
    
    class Meta:
        unique_together = ['user', 'destination']
    
    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.destination.name}"
