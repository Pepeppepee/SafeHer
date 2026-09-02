from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from experiences.models import Experience
from .models import TripIntent, BuddyThread, BuddyThreadMember, BuddyMessage, Report
from .serializers import (
    TripIntentCreateSerializer, BuddyThreadListSerializer, BuddyThreadDetailSerializer,
    BuddyMessageSerializer, SendMessageSerializer, ReportSerializer,
)

MAX_MEMBERS = 4


def _find_or_create_thread(experience, intended_date, user):
    """
    Blind matching: same experience, same date, both opted in.
    Joins an open thread if one exists, otherwise pairs up with
    another waiting woman, otherwise she waits alone.
    """
    open_thread = (
        BuddyThread.objects.filter(experience=experience, trip_date=intended_date, is_active=True)
        .annotate(n=Count("members"))
        .filter(n__lt=MAX_MEMBERS)
        .exclude(members__user=user)
        .order_by("created_at")
        .first()
    )
    if open_thread:
        BuddyThreadMember.objects.get_or_create(thread=open_thread, user=user)
        return open_thread

    waiting_intent = (
        TripIntent.objects.filter(
            experience=experience, intended_date=intended_date, wants_buddy=True, matched=False
        )
        .exclude(user=user)
        .order_by("created_at")
        .first()
    )
    if waiting_intent:
        thread = BuddyThread.objects.create(experience=experience, trip_date=intended_date)
        BuddyThreadMember.objects.create(thread=thread, user=waiting_intent.user)
        BuddyThreadMember.objects.create(thread=thread, user=user)
        waiting_intent.matched = True
        waiting_intent.save(update_fields=["matched"])
        return thread

    return None


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_intent(request):
    s = TripIntentCreateSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    try:
        experience = Experience.objects.get(id=s.validated_data["experience_id"])
    except Experience.DoesNotExist:
        return Response({"error": "Experience not found"}, status=404)

    intent, _ = TripIntent.objects.update_or_create(
        user=request.user, experience=experience, intended_date=s.validated_data["intended_date"],
        defaults={"wants_buddy": s.validated_data["wants_buddy"]},
    )

    thread = None
    if intent.wants_buddy:
        if intent.matched:
            # Already matched from an earlier call — return her existing thread, don't re-match.
            thread = BuddyThread.objects.filter(
                experience=experience, trip_date=intent.intended_date, members__user=request.user
            ).first()
        else:
            thread = _find_or_create_thread(experience, intent.intended_date, request.user)
            if thread:
                intent.matched = True
                intent.save(update_fields=["matched"])

    return Response({
        "intent_id": str(intent.id),
        "wants_buddy": intent.wants_buddy,
        "matched": intent.matched,
        "thread": BuddyThreadListSerializer(thread, context={"request": request}).data if thread else None,
    }, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_threads(request):
    now = timezone.now()
    threads = (
        BuddyThread.objects.filter(members__user=request.user, is_active=True, expires_at__gt=now)
        .distinct()
        .order_by("-created_at")
    )
    return Response(BuddyThreadListSerializer(threads, many=True, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def thread_detail(request, thread_id):
    try:
        thread = BuddyThread.objects.get(id=thread_id, members__user=request.user)
    except BuddyThread.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    return Response(BuddyThreadDetailSerializer(thread, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, thread_id):
    try:
        thread = BuddyThread.objects.get(id=thread_id, members__user=request.user)
    except BuddyThread.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    if thread.is_expired or not thread.is_active:
        return Response({"error": "This chat has expired"}, status=400)

    s = SendMessageSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    msg = BuddyMessage.objects.create(thread=thread, sender=request.user, content=s.validated_data["content"])
    return Response(BuddyMessageSerializer(msg, context={"request": request}).data, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def report_user(request, thread_id):
    try:
        thread = BuddyThread.objects.get(id=thread_id, members__user=request.user)
    except BuddyThread.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    s = ReportSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    reported_id = s.validated_data["reported_user_id"]
    if str(reported_id) == str(request.user.id):
        return Response({"error": "You can't report yourself"}, status=400)
    if not BuddyThreadMember.objects.filter(thread=thread, user_id=reported_id).exists():
        return Response({"error": "That person isn't in this chat"}, status=400)

    Report.objects.get_or_create(
        reporter=request.user, reported_user_id=reported_id, thread=thread,
        defaults={"reason": s.validated_data["reason"], "note": s.validated_data.get("note", "")},
    )

    distinct_reporters = Report.objects.filter(reported_user_id=reported_id).values("reporter").distinct().count()
    if distinct_reporters >= 2:
        from accounts.models import User
        User.objects.filter(id=reported_id).update(is_banned=True)

    return Response({"message": "Thank you, we've received your report."}, status=201)
