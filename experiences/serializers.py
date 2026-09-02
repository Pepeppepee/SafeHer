from rest_framework import serializers
from .models import Experience, VibeWindow, SafetyIntel, VerifiedStay

class VibeWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = VibeWindow
        fields = ["day_type", "time_start", "time_end", "crowd_level", "vibe_notes", "solo_comfortable"]

class SafetyIntelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyIntel
        fields = ["category", "content", "safe_until", "transport_back", "source_type", "verified_date"]

class VerifiedStaySerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedStay
        fields = ["name", "stay_type", "price_range", "verification_note"]

class ExperienceListSerializer(serializers.ModelSerializer):
    safety_percentage = serializers.ReadOnlyField()
    class Meta:
        model = Experience
        fields = ["id", "name", "area", "scene_type", "vibe_tags", "solo_difficulty", "budget_tier", "total_visitors", "felt_safe_count", "safety_percentage"]

class ExperienceDetailSerializer(serializers.ModelSerializer):
    safety_percentage = serializers.ReadOnlyField()
    vibe_windows = VibeWindowSerializer(many=True, read_only=True)
    safety_intel = SafetyIntelSerializer(many=True, read_only=True)
    verified_stays = VerifiedStaySerializer(many=True, read_only=True)
    match_score = serializers.FloatField(read_only=True, required=False, default=None)
    match_reasons = serializers.ListField(read_only=True, required=False, default=[])
    class Meta:
        model = Experience
        fields = ["id", "name", "area", "scene_type", "description", "latitude", "longitude", "vibe_tags", "solo_difficulty", "min_comfort_tier", "budget_tier", "total_visitors", "felt_safe_count", "safety_percentage", "vibe_windows", "safety_intel", "verified_stays", "match_score", "match_reasons"]
