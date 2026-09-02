from rest_framework import serializers
from .models import MoodQuery, MoodResponse

class MoodQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodQuery
        fields = ["id", "mood", "crowd_preference", "distance", "scene_preference", "created_at"]
        read_only_fields = ["id", "created_at"]

class MoodResponseCreateSerializer(serializers.Serializer):
    experience_id = serializers.UUIDField()
    mood_query_id = serializers.UUIDField()
    decision = serializers.ChoiceField(choices=["going", "declined", "skipped"])
    decline_reason = serializers.CharField(required=False, allow_blank=True)
    decline_note = serializers.CharField(required=False, allow_blank=True)

class CheckInSerializer(serializers.Serializer):
    visited = serializers.BooleanField()
    visit_mood_match = serializers.IntegerField(min_value=1, max_value=5, required=False)
    visit_safety_score = serializers.IntegerField(min_value=1, max_value=5, required=False)
    visit_note = serializers.CharField(required=False, allow_blank=True)
    would_recommend = serializers.BooleanField(required=False)
    share_review = serializers.BooleanField(required=False, default=False)

class MoodResponseSerializer(serializers.ModelSerializer):
    experience_name = serializers.CharField(source="experience.name", read_only=True)
    class Meta:
        model = MoodResponse
        fields = ["id", "experience", "experience_name", "decision", "decline_reason", "visited", "visit_mood_match", "visit_safety_score", "visit_note", "would_recommend", "recommended_at", "checked_in_at"]
