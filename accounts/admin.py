from django.contrib import admin
from .models import User, InviteCode, OTPVerification, TravelerProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "phone", "valley_area", "is_verified", "is_banned", "created_at"]
    list_filter = ["is_verified", "is_banned", "valley_area"]
    search_fields = ["first_name", "phone"]
    readonly_fields = ["id", "created_at"]

@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "created_by", "used_by", "is_active", "created_at"]
    list_filter = ["is_active"]

@admin.register(TravelerProfile)
class TravelerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "comfort_tier", "trips_completed", "personality_label"]
    list_filter = ["comfort_tier"]

admin.site.register(OTPVerification)
