from django.contrib import admin
from .models import Experience, VibeWindow, SafetyIntel, VerifiedStay

class VibeWindowInline(admin.TabularInline):
    model = VibeWindow
    extra = 1

class SafetyIntelInline(admin.StackedInline):
    model = SafetyIntel
    extra = 1

class VerifiedStayInline(admin.TabularInline):
    model = VerifiedStay
    extra = 0

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["name", "area", "solo_difficulty", "min_comfort_tier", "total_visitors", "safety_percentage", "is_active"]
    list_filter = ["is_active", "min_comfort_tier", "budget_tier"]
    search_fields = ["name", "area"]
    inlines = [VibeWindowInline, SafetyIntelInline, VerifiedStayInline]
