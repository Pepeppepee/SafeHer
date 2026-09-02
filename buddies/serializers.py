from rest_framework import serializers
from .models import TripIntent, BuddyThread, BuddyThreadMember, BuddyMessage, Report


class TripIntentCreateSerializer(serializers.Serializer):
    experience_id = serializers.UUIDField()
    intended_date = serializers.DateField()
    wants_buddy = serializers.BooleanField(default=False)


class BuddyMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.first_name", read_only=True)
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = BuddyMessage
        fields = ["id", "sender_name", "is_me", "content", "sent_at"]

    def get_is_me(self, obj):
        request = self.context.get("request")
        return bool(request and obj.sender_id == request.user.id)


class BuddyThreadListSerializer(serializers.ModelSerializer):
    experience_name = serializers.CharField(source="experience.name", read_only=True)
    experience_area = serializers.CharField(source="experience.area", read_only=True)
    member_count = serializers.IntegerField(source="members.count", read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = BuddyThread
        fields = ["id", "experience_name", "experience_area", "trip_date",
                  "member_count", "expires_at", "last_message"]

    def get_last_message(self, obj):
        msg = obj.messages.order_by("-sent_at").first()
        if not msg:
            return None
        return {"sender_name": msg.sender.first_name, "content": msg.content}


class BuddyThreadDetailSerializer(serializers.ModelSerializer):
    experience_name = serializers.CharField(source="experience.name", read_only=True)
    experience_area = serializers.CharField(source="experience.area", read_only=True)
    members = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = BuddyThread
        fields = ["id", "experience_name", "experience_area", "trip_date",
                  "expires_at", "members", "messages"]

    def get_members(self, obj):
        request = self.context.get("request")
        return [
            {"id": str(m.user_id), "first_name": m.user.first_name,
             "is_me": bool(request and m.user_id == request.user.id)}
            for m in obj.members.select_related("user")
        ]

    def get_messages(self, obj):
        return BuddyMessageSerializer(
            obj.messages.select_related("sender"), many=True, context=self.context
        ).data


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=500, trim_whitespace=True)

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message can't be empty.")
        if "http://" in value or "https://" in value or "www." in value:
            raise serializers.ValidationError("Links aren't allowed in buddy chat.")
        return value


class ReportSerializer(serializers.Serializer):
    reported_user_id = serializers.UUIDField()
    reason = serializers.ChoiceField(choices=[c[0] for c in Report.REASONS])
    note = serializers.CharField(max_length=300, required=False, allow_blank=True)
