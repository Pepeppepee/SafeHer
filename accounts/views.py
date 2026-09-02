from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.utils import timezone
from .models import User, InviteCode, TravelerProfile
from .serializers import InviteVerifySerializer, SignupSerializer, ProfileSetupSerializer, TravelerProfileSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_invite(request):
    s = InviteVerifySerializer(data=request.data)
    s.is_valid(raise_exception=True)
    return Response({"valid": True, "code": s.validated_data["code"]})

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    s = SignupSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    code_str = s.validated_data["invite_code"].upper()
    phone = s.validated_data["phone"]
    first_name = s.validated_data["first_name"]
    try:
        invite = InviteCode.objects.get(code=code_str, is_active=True, used_by__isnull=True)
    except InviteCode.DoesNotExist:
        return Response({"error": "Invalid invite code"}, status=400)
    if User.objects.filter(phone=phone).exists():
        return Response({"error": "Phone already registered"}, status=400)
    user = User.objects.create_user(phone=phone, first_name=first_name, invited_by=invite.created_by)
    user.is_verified = True
    user.save()
    invite.used_by = user
    invite.used_at = timezone.now()
    invite.is_active = False
    invite.save()
    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"id": str(user.id), "first_name": user.first_name, "message": "Welcome!", "token": token.key}, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])
def quick_login(request):
    phone = request.data.get("phone")
    try:
        user = User.objects.get(phone=phone, is_banned=False)
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        has_profile = TravelerProfile.objects.filter(user=user).exists()
        return Response({"id": str(user.id), "first_name": user.first_name, "has_profile": has_profile, "token": token.key})
    except User.DoesNotExist:
        return Response({"error": "No account found. Need an invite code."}, status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def setup_profile(request):
    s = ProfileSetupSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    profile, created = TravelerProfile.objects.update_or_create(
        user=request.user,
        defaults={"comfort_tier": s.validated_data["comfort_tier"], "anxiety_points": s.validated_data["anxiety_points"], "interest_scores": s.validated_data.get("interest_scores", {})}
    )
    return Response(TravelerProfileSerializer(profile).data, status=201 if created else 200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    try:
        return Response(TravelerProfileSerializer(request.user.profile).data)
    except TravelerProfile.DoesNotExist:
        return Response({"error": "Profile not set up yet"}, status=404)
