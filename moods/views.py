from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import MoodQuery, MoodResponse
from .matcher import match_experiences
from .serializers import MoodQuerySerializer, MoodResponseCreateSerializer, CheckInSerializer, MoodResponseSerializer
from experiences.serializers import ExperienceDetailSerializer
from accounts.models import TravelerProfile

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def find_match(request):
    s = MoodQuerySerializer(data=request.data)
    s.is_valid(raise_exception=True)
    query = MoodQuery.objects.create(user=request.user, **s.validated_data)
    try:
        profile = request.user.profile
    except TravelerProfile.DoesNotExist:
        return Response({"error": "Set up your profile first"}, status=400)
    results = match_experiences(profile, query, limit=5)
    if not results:
        return Response({"query": MoodQuerySerializer(query).data, "match": None, "message": "No matches for your mood right now. Try a different mood or distance."})
    matches = []
    for exp, score, reasons in results:
        exp.match_score = score
        exp.match_reasons = reasons
        matches.append(ExperienceDetailSerializer(exp).data)
    top_exp = results[0][0]
    reviews = MoodResponse.objects.filter(experience=top_exp, share_review=True, visit_note__gt="").values_list("visit_note", flat=True)[:3]
    return Response({"query": MoodQuerySerializer(query).data, "match": matches[0], "alternatives": matches[1:], "reviews": list(reviews)})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def respond_to_match(request):
    s = MoodResponseCreateSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    response = MoodResponse.objects.create(user=request.user, experience_id=s.validated_data["experience_id"], mood_query_id=s.validated_data["mood_query_id"], decision=s.validated_data["decision"], decline_reason=s.validated_data.get("decline_reason", ""), decline_note=s.validated_data.get("decline_note", ""))
    msg = {"going": "Have a beautiful time!", "declined": "No worries.", "skipped": "Let us try another."}
    return Response({"id": str(response.id), "decision": response.decision, "message": msg.get(response.decision, "")}, status=201)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_in(request, response_id):
    try:
        mood_response = MoodResponse.objects.get(id=response_id, user=request.user)
    except MoodResponse.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    s = CheckInSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    mood_response.visited = s.validated_data["visited"]
    mood_response.checked_in_at = timezone.now()
    if s.validated_data["visited"]:
        mood_response.visit_mood_match = s.validated_data.get("visit_mood_match")
        mood_response.visit_safety_score = s.validated_data.get("visit_safety_score")
        mood_response.visit_note = s.validated_data.get("visit_note", "")
        mood_response.would_recommend = s.validated_data.get("would_recommend")
        mood_response.share_review = s.validated_data.get("share_review", False)
        exp = mood_response.experience
        exp.total_visitors += 1
        if mood_response.visit_safety_score and mood_response.visit_safety_score >= 4:
            exp.felt_safe_count += 1
        exp.save()
        profile = request.user.profile
        profile.trips_completed += 1
        if profile.trips_completed >= 5 and profile.comfort_tier == "first_timer":
            profile.comfort_tier = "cautious"
        elif profile.trips_completed >= 15 and profile.comfort_tier == "cautious":
            profile.comfort_tier = "confident"
        profile.save()
    mood_response.save()
    return Response({"message": "Thank you!", "trips_completed": request.user.profile.trips_completed, "personality_label": request.user.profile.personality_label})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_checkins(request):
    pending = MoodResponse.objects.filter(user=request.user, decision="going", visited__isnull=True).select_related("experience")
    return Response(MoodResponseSerializer(pending, many=True).data)
