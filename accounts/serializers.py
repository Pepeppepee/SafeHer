from rest_framework import serializers
from .models import User, InviteCode, TravelerProfile

class InviteVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=8)
    def validate_code(self, value):
        try:
            InviteCode.objects.get(code=value.upper(), is_active=True, used_by__isnull=True)
        except InviteCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or already used invite code.")
        return value

class SignupSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=8)
    phone = serializers.CharField(max_length=15)
    first_name = serializers.CharField(max_length=30)

class ProfileSetupSerializer(serializers.Serializer):
    comfort_tier = serializers.ChoiceField(choices=["first_timer", "cautious", "confident"])
    anxiety_points = serializers.ListField(child=serializers.CharField(), max_length=5)
    interest_scores = serializers.DictField(child=serializers.FloatField(), required=False)

class TravelerProfileSerializer(serializers.ModelSerializer):
    personality_label = serializers.ReadOnlyField()
    class Meta:
        model = TravelerProfile
        fields = ["comfort_tier", "anxiety_points", "interest_scores", "trips_completed", "personality_label"]

class MyInviteCodeSerializer(serializers.ModelSerializer):
    used_by_name = serializers.SerializerMethodField()
    class Meta:
        model = InviteCode
        fields = ["code", "is_active", "used_by_name", "created_at"]

    def get_used_by_name(self, obj):
        return obj.used_by.first_name if obj.used_by_id else None
