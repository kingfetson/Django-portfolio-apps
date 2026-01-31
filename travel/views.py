from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Destination, Trip, TravelTip
from django.db.models import Count

def travel_home(request):
    """Travel app homepage"""
    featured_destinations = Destination.objects.all()[:6]
    featured_trips = Trip.objects.filter(featured=True)[:4]
    travel_tips = TravelTip.objects.filter(featured=True)[:3]
    
    # Get destinations with most trips
    popular_destinations = Destination.objects.annotate(
        trip_count=Count('trips')
    ).order_by('-trip_count')[:4]
    
    context = {
        'featured_destinations': featured_destinations,
        'featured_trips': featured_trips,
        'travel_tips': travel_tips,
        'popular_destinations': popular_destinations,
    }
    return render(request, 'travel/index.html', context)

def destination_list(request):
    """List all destinations"""
    continents = Destination.CONTINENT_CHOICES
    selected_continent = request.GET.get('continent', '')
    
    destinations = Destination.objects.all()
    
    if selected_continent:
        destinations = destinations.filter(continent=selected_continent)
    
    # Order by name
    destinations = destinations.order_by('name')
    
    context = {
        'destinations': destinations,
        'continents': continents,
        'selected_continent': selected_continent,
    }
    return render(request, 'travel/destinations.html', context)

def destination_detail(request, slug):
    """Destination detail page"""
    destination = get_object_or_404(Destination, slug=slug)
    trips = destination.trips.all()
    
    context = {
        'destination': destination,
        'trips': trips,
    }
    return render(request, 'travel/destination_detail.html', context)

def trip_list(request):
    """List all trips"""
    trip_types = Trip.TRIP_TYPE_CHOICES
    selected_type = request.GET.get('type', '')
    
    trips = Trip.objects.all()
    
    if selected_type:
        trips = trips.filter(trip_type=selected_type)
    
    # Filter by featured if requested
    if request.GET.get('featured'):
        trips = trips.filter(featured=True)
    
    context = {
        'trips': trips,
        'trip_types': trip_types,
        'selected_type': selected_type,
    }
    return render(request, 'travel/trips.html', context)

def trip_detail(request, slug):
    """Trip detail page"""
    trip = get_object_or_404(Trip, slug=slug)
    photos = trip.photos.all()
    
    # Parse highlights into list
    highlights = [h.strip() for h in trip.highlights.split('\n') if h.strip()]
    
    # Parse itinerary into list of days
    itinerary_days = []
    for i, day in enumerate(trip.itinerary.split('\n'), 1):
        if day.strip():
            itinerary_days.append({'day': i, 'description': day.strip()})
    
    context = {
        'trip': trip,
        'photos': photos,
        'highlights': highlights,
        'itinerary_days': itinerary_days,
    }
    return render(request, 'travel/trip_detail.html', context)

def travel_tips(request):
    """Travel tips and advice"""
    categories = TravelTip.CATEGORY_CHOICES
    selected_category = request.GET.get('category', '')
    
    tips = TravelTip.objects.all()
    
    if selected_category:
        tips = tips.filter(category=selected_category)
    
    # Group tips by category for display
    tips_by_category = {}
    for tip in tips:
        category_name = dict(categories).get(tip.category, tip.category)
        if category_name not in tips_by_category:
            tips_by_category[category_name] = []
        tips_by_category[category_name].append(tip)
    
    context = {
        'tips_by_category': tips_by_category,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'travel/tips.html', context)

@login_required
def my_wishlist(request):
    """User's travel wishlist"""
    wishlist_items = request.user.travel_wishlist.all()
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'travel/wishlist.html', context)
