from django.contrib import admin
from .models import TripIntent, BuddyThread, BuddyThreadMember, BuddyMessage, Report

@admin.register(TripIntent)
class TripIntentAdmin(admin.ModelAdmin):
    list_display = ["user", "experience", "intended_date", "wants_buddy", "matched"]
    list_filter = ["wants_buddy", "matched"]

@admin.register(BuddyThread)
class BuddyThreadAdmin(admin.ModelAdmin):
    list_display = ["experience", "trip_date", "is_active", "expires_at"]
    list_filter = ["is_active"]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["reporter", "reported_user", "reason", "created_at"]
    list_filter = ["reason"]

admin.site.register(BuddyThreadMember)
admin.site.register(BuddyMessage)
