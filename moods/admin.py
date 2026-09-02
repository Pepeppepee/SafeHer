from django.contrib import admin
from .models import MoodQuery, MoodResponse

@admin.register(MoodQuery)
class MoodQueryAdmin(admin.ModelAdmin):
    list_display = ["user", "mood", "crowd_preference", "distance", "created_at"]
    list_filter = ["mood", "crowd_preference"]

@admin.register(MoodResponse)
class MoodResponseAdmin(admin.ModelAdmin):
    list_display = ["user", "experience", "decision", "decline_reason", "visited", "visit_mood_match", "visit_safety_score"]
    list_filter = ["decision", "visited"]
