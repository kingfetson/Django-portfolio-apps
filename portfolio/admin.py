from django.contrib import admin
from .models import Portfolio

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'email', 'created_at')
    search_fields = ('user__username', 'title', 'email')