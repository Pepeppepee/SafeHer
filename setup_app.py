"""
Run this once: python setup_app.py
It creates all missing files for the app.
"""
import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {path}")

print("Setting up SafeHer app files...\n")

# 1. settings.py - update TEMPLATES dirs
write("safeher/settings.py", '''from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "change-me-in-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","accounts","experiences","moods","buddies",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "safeher.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "safeher.wsgi.application"
DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR / "db.sqlite3"}}
AUTH_USER_MODEL = "accounts.User"
REST_FRAMEWORK = {"DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination","PAGE_SIZE":10}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
''')

# 2. Main urls.py
write("safeher/urls.py", '''from django.contrib import admin
from django.urls import path, include
from experiences.views import app_view

urlpatterns = [
    path("", app_view, name="app"),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/moods/", include("moods.urls")),
]
''')

# 3. accounts/urls.py
write("accounts/urls.py", '''from django.urls import path
from . import views
urlpatterns = [
    path("verify-invite/", views.verify_invite),
    path("signup/", views.signup),
    path("login/", views.quick_login),
    path("profile/setup/", views.setup_profile),
    path("profile/", views.my_profile),
]
''')

# 4. accounts/serializers.py
write("accounts/serializers.py", '''from rest_framework import serializers
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
''')

# 5. accounts/views.py
write("accounts/views.py", '''from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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
    return Response({"id": str(user.id), "first_name": user.first_name, "message": "Welcome!"}, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])
def quick_login(request):
    phone = request.data.get("phone")
    try:
        user = User.objects.get(phone=phone, is_banned=False)
        login(request, user)
        has_profile = TravelerProfile.objects.filter(user=user).exists()
        return Response({"id": str(user.id), "first_name": user.first_name, "has_profile": has_profile})
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
''')

# 6. experiences/serializers.py
write("experiences/serializers.py", '''from rest_framework import serializers
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
        fields = ["id", "name", "area", "vibe_tags", "solo_difficulty", "budget_tier", "total_visitors", "felt_safe_count", "safety_percentage"]

class ExperienceDetailSerializer(serializers.ModelSerializer):
    safety_percentage = serializers.ReadOnlyField()
    vibe_windows = VibeWindowSerializer(many=True, read_only=True)
    safety_intel = SafetyIntelSerializer(many=True, read_only=True)
    verified_stays = VerifiedStaySerializer(many=True, read_only=True)
    match_score = serializers.FloatField(read_only=True, required=False, default=None)
    match_reasons = serializers.ListField(read_only=True, required=False, default=[])
    class Meta:
        model = Experience
        fields = ["id", "name", "area", "description", "latitude", "longitude", "vibe_tags", "solo_difficulty", "min_comfort_tier", "budget_tier", "total_visitors", "felt_safe_count", "safety_percentage", "vibe_windows", "safety_intel", "verified_stays", "match_score", "match_reasons"]
''')

# 7. experiences/views.py
write("experiences/views.py", '''from django.shortcuts import render

def app_view(request):
    return render(request, "app.html")
''')

# 8. moods/urls.py
write("moods/urls.py", '''from django.urls import path
from . import views
urlpatterns = [
    path("find/", views.find_match),
    path("respond/", views.respond_to_match),
    path("checkin/<uuid:response_id>/", views.check_in),
    path("pending/", views.pending_checkins),
]
''')

# 9. moods/serializers.py
write("moods/serializers.py", '''from rest_framework import serializers
from .models import MoodQuery, MoodResponse

class MoodQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodQuery
        fields = ["id", "mood", "crowd_preference", "distance", "created_at"]
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
''')

# 10. moods/views.py
write("moods/views.py", '''from rest_framework import status
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
''')

# 11. moods/matcher.py
write("moods/matcher.py", '''from experiences.models import Experience, VibeWindow
from datetime import datetime

COMFORT_ORDER = {"first_timer": 1, "cautious": 2, "confident": 3}
MOOD_TO_VIBES = {"peace": ["peaceful", "contemplative", "romantic"], "energy": ["energetic", "social"], "wonder": ["adventurous", "cozy"], "reset": ["peaceful", "contemplative"]}
CROWD_MAP = {"quiet": ["low"], "social": ["medium", "high"]}

def match_experiences(profile, mood_query, limit=5):
    experiences = Experience.objects.filter(is_active=True).prefetch_related("vibe_windows", "safety_intel")
    scored = []
    for exp in experiences:
        exp_min = COMFORT_ORDER.get(exp.min_comfort_tier, 1)
        user_comfort = COMFORT_ORDER.get(profile.comfort_tier, 1)
        if user_comfort < exp_min:
            continue
        score = 0.0
        reasons = []
        target_vibes = MOOD_TO_VIBES.get(mood_query.mood, [])
        vibe_overlap = set(exp.vibe_tags) & set(target_vibes)
        if vibe_overlap:
            vibe_score = len(vibe_overlap) / max(len(target_vibes), 1)
            score += vibe_score * 40
            reasons.append(f"Matches your {mood_query.mood} mood")
        else:
            continue
        now = datetime.now().time()
        today = "weekend" if datetime.now().weekday() >= 5 else "weekday"
        windows = exp.vibe_windows.filter(day_type__in=[today, "any"], time_start__lte=now, time_end__gte=now)
        preferred_crowds = CROWD_MAP.get(mood_query.crowd_preference, [])
        for w in windows:
            if w.crowd_level in preferred_crowds:
                score += 20
                reasons.append(f"{w.crowd_level.title()} crowd right now")
                if w.solo_comfortable:
                    score += 10
                    reasons.append("Solo comfortable")
                break
        if exp.total_visitors > 0:
            safety_ratio = exp.felt_safe_count / exp.total_visitors
            score += safety_ratio * 20
            if safety_ratio >= 0.8:
                reasons.append(f"{exp.felt_safe_count}/{exp.total_visitors} women felt safe")
        score += 5
        anxiety_penalty = 0
        for point in profile.anxiety_points:
            if point == "Empty streets" and exp.solo_difficulty >= 4:
                anxiety_penalty += 10
            if point == "No signal":
                if not exp.safety_intel.filter(category="connectivity").exists():
                    anxiety_penalty += 5
        score -= anxiety_penalty
        if score > 0:
            scored.append((exp, round(score, 1), reasons))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]
''')

# 12. templates/app.html — the frontend
APP_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>SafeHer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#FDFAF6;max-width:430px;margin:0 auto;min-height:100vh}
:root{--a:#2D7A5F;--al:#E8F5EE;--ad:#1B5E43;--t:#1A1A1A;--ts:#6B6B6B;--tm:#9B9B9B;--b:#E8E5DE;--c:#fff;--s:#E8F5EE;--st:#1B5E43;--w:#F4E8D1;--wd:#8B6914}
.screen{display:none;padding:20px 16px 32px}.screen.active{display:block}
h1{font-size:22px;font-weight:600;color:var(--t);margin-bottom:8px}
.sub{font-size:14px;color:var(--ts);margin-bottom:24px;line-height:1.5}
.btn{width:100%;padding:14px;border-radius:999px;border:none;background:var(--a);color:#fff;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit}
.btn-o{background:transparent;border:1.5px solid #D1CEC7;color:var(--t)}
.btn-s{background:var(--al);color:var(--ad);border:none}
.btn:disabled{opacity:.4}
.br{display:flex;gap:8px}.br>div{flex:1}
input,textarea{width:100%;padding:14px 16px;border-radius:12px;border:1.5px solid var(--b);font-size:15px;background:var(--c);outline:none;font-family:inherit;box-sizing:border-box}
.mg{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px}
.mc{padding:16px 14px;border-radius:14px;border:1.5px solid var(--b);background:var(--c);cursor:pointer;transition:all .15s}
.mc.s{border-color:var(--a);background:var(--al)}
.mc .e{font-size:22px}.mc .n{font-size:15px;font-weight:600;margin:6px 0 2px}.mc .d{font-size:11px;color:var(--tm)}
.ch{display:inline-block;padding:8px 16px;border-radius:999px;border:1.5px solid var(--b);background:var(--c);cursor:pointer;font-size:13px;margin:0 6px 8px 0;transition:all .15s}
.ch.s{border-color:var(--a);background:var(--al);color:var(--ad);font-weight:600}
.op{padding:14px 16px;border-radius:12px;border:1.5px solid var(--b);background:var(--c);cursor:pointer;margin-bottom:10px;font-size:14px;transition:all .15s}
.op.s{border-color:var(--a);background:var(--al);color:var(--ad);font-weight:600}
.tag{display:inline-block;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:500;background:var(--al);color:var(--ad);margin-right:6px;margin-bottom:6px}
.tw{background:var(--w);color:var(--wd)}
.card{background:var(--c);border-radius:16px;border:1px solid var(--b);overflow:hidden}
.ch2{height:120px;background:linear-gradient(135deg,#2D7A5F,#5BA88A,#F4E8D1);display:flex;align-items:flex-end;padding:16px}
.ch2 h2{font-size:18px;font-weight:700;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.3)}
.ch2 p{font-size:13px;color:rgba(255,255,255,.9)}
.cb{padding:16px}
.ib{background:#FDFAF6;border-radius:10px;padding:12px;margin-bottom:10px;font-size:13px;line-height:1.6}
.sb{background:var(--s);border-radius:10px;padding:12px;margin-bottom:10px}
.sb .tt{font-size:14px;font-weight:600;color:var(--st);margin-bottom:6px}
.sb p{font-size:13px;color:var(--st);line-height:1.5;margin-bottom:4px}
.sb .st2{font-size:12px;opacity:.8}
.rb{background:#FDFAF6;border-radius:10px;padding:12px;margin-bottom:14px}
.rb .q{font-size:13px;color:var(--ts);font-style:italic;margin-bottom:4px}
.rb .at{font-size:11px;color:var(--tm)}
.sr{display:flex;gap:8px;justify-content:center;margin:16px 0}
.sb2{width:48px;height:48px;border-radius:50%;border:2px solid var(--b);background:var(--c);font-size:18px;cursor:pointer;font-weight:600;color:var(--ts);font-family:inherit}
.sb2.s{border-color:var(--a);background:var(--al);color:var(--ad)}
.lb{font-size:13px;color:var(--ts);margin-bottom:8px}
.mt16{margin-top:16px}.mt20{margin-top:20px}.ctr{text-align:center}.p40{padding-top:40px}.p60{padding-top:60px}
.err{background:#FEE8E7;color:#9B2C2C;padding:12px;border-radius:10px;font-size:13px;margin-top:16px;display:none}
</style>
</head>
<body>

<div class="screen active" id="loginScreen">
<div class="p60 ctr">
<p style="font-size:32px;margin-bottom:8px">🌿</p>
<h1>SafeHer</h1>
<p class="sub">Tell me your mood. I'll find your place.</p>
</div>
<input type="tel" id="loginPhone" placeholder="Your phone number" style="margin-bottom:12px">
<button class="btn" onclick="doLogin()">Enter</button>
<p style="font-size:12px;color:var(--tm);text-align:center;margin-top:16px">For demo, use the phone you registered in admin.</p>
<div id="loginError" class="err"></div>
</div>

<div class="screen" id="setupScreen">
<h1>Quick setup</h1>
<p class="sub">Two questions so we match you right.</p>
<p class="lb">How experienced are you solo?</p>
<div id="cOpts">
<div class="op" data-v="first_timer" onclick="pC(this)">Never been out alone</div>
<div class="op" data-v="cautious" onclick="pC(this)">I have, but I'm careful</div>
<div class="op" data-v="confident" onclick="pC(this)">I go solo all the time</div>
</div>
<p class="lb mt16">What makes you uneasy? (up to 3)</p>
<div id="aChips">
<span class="ch" onclick="tA(this)">Empty streets</span>
<span class="ch" onclick="tA(this)">Men staring</span>
<span class="ch" onclick="tA(this)">No signal</span>
<span class="ch" onclick="tA(this)">Hard to get back</span>
<span class="ch" onclick="tA(this)">Being alone</span>
</div>
<button class="btn mt20" id="sBtn" disabled onclick="doSetup()">Done — show me places</button>
</div>

<div class="screen" id="moodScreen">
<h1 id="mG">How do you want to feel today?</h1>
<p class="lb" id="mT"></p>
<div class="mg">
<div class="mc" onclick="pM(this,'peace')"><span class="e">🌅</span><p class="n">Peace</p><p class="d">stillness, sunsets, breathe</p></div>
<div class="mc" onclick="pM(this,'energy')"><span class="e">⚡</span><p class="n">Energy</p><p class="d">concerts, crowds, buzz</p></div>
<div class="mc" onclick="pM(this,'wonder')"><span class="e">✨</span><p class="n">Wonder</p><p class="d">new streets, hidden gems</p></div>
<div class="mc" onclick="pM(this,'reset')"><span class="e">🍃</span><p class="n">Reset</p><p class="d">river, silence, nothing</p></div>
</div>
<p class="lb">I'd rather be</p>
<div style="margin-bottom:16px">
<span class="ch" onclick="pCr(this,'quiet')">Somewhere quiet</span>
<span class="ch" onclick="pCr(this,'social')">Around people</span>
</div>
<p class="lb">How far?</p>
<div style="margin-bottom:24px">
<span class="ch" onclick="pD(this,'walkable')">Walkable</span>
<span class="ch" onclick="pD(this,'under_1hr')">Under 1hr</span>
<span class="ch" onclick="pD(this,'day_trip')">Day trip</span>
</div>
<button class="btn" id="fBtn" disabled onclick="doFind()">Find my place</button>
</div>

<div class="screen" id="loadScreen"><div style="text-align:center;padding:80px 20px;color:var(--ts)"><p style="font-size:32px;margin-bottom:16px">🔍</p><p>Finding the perfect place...</p></div></div>

<div class="screen" id="matchScreen">
<p style="font-size:12px;color:var(--tm);letter-spacing:.5px;text-transform:uppercase;margin-bottom:12px">Your match</p>
<div class="card">
<div class="ch2"><div><h2 id="mN"></h2><p id="mA"></p></div></div>
<div class="cb">
<div id="mTags" style="margin-bottom:14px"></div>
<div class="ib" id="mInfo"></div>
<div class="sb" id="mSafe"></div>
<div id="mRevs"></div>
<div class="br"><div><button class="btn" onclick="doR('going')">I'm going</button></div><div><button class="btn btn-o" onclick="show('decScreen')">Not this time</button></div></div>
</div></div>
</div>

<div class="screen" id="decScreen">
<h1 style="font-size:20px">What didn't fit?</h1>
<p class="sub">Helps us get it right.</p>
<div class="op" onclick="doD(this,'wrong_mood')">Wrong mood</div>
<div class="op" onclick="doD(this,'too_far')">Too far</div>
<div class="op" onclick="doD(this,'not_safe')">Doesn't feel safe</div>
<div class="op" onclick="doD(this,'been_there')">Already been</div>
<div class="op" onclick="doD(this,'bad_timing')">Bad timing</div>
</div>

<div class="screen" id="goScreen">
<div class="p40 ctr">
<p style="font-size:40px;margin-bottom:12px">🎉</p>
<h1>Have a beautiful time!</h1>
<p class="sub">We'll check in after your visit.</p>
<button class="btn" onclick="showMood()">Find another place</button>
<button class="btn btn-o mt16" onclick="showCI()">Check in on a past trip</button>
</div>
</div>

<div class="screen" id="ciScreen">
<div class="p40">
<h1 style="font-size:20px" id="ciT">Did you make it?</h1>
<div class="br mt20" id="ci1"><div><button class="btn" onclick="ciYes()">Yes, I went!</button></div><div><button class="btn btn-o" onclick="showMood()">Not yet</button></div></div>
<div id="ci2" style="display:none">
<p class="lb mt16">Did it match the mood you wanted?</p>
<div class="sr" id="msR"></div>
<p class="lb mt16">How safe did you feel?</p>
<div class="sr" id="ssR"></div>
<textarea id="ciN" rows="3" placeholder="Anything other women should know? (optional)" style="margin-top:16px"></textarea>
<div style="margin-top:8px"><label style="font-size:13px;color:var(--ts);cursor:pointer"><input type="checkbox" id="shR"> Share anonymously with other women</label></div>
<button class="btn mt20" id="ciBtn" disabled onclick="doCI()">Submit</button>
</div></div>
</div>

<div class="screen" id="thxScreen">
<div class="p60 ctr">
<p style="font-size:40px;margin-bottom:12px">💛</p>
<h1>Thank you!</h1>
<p class="sub">Your experience helps other women.</p>
<p style="font-size:13px;color:var(--tm);margin-bottom:32px" id="thxL"></p>
<button class="btn" onclick="showMood()">Find another place</button>
</div>
</div>

<script>
let cU=null,cMo=null,cCr=null,cDi=null,cCo=null,cAn=[],cMa=null,cQI=null,cRI=null,ciM=null,ciS=null;
function gC(n){let v=document.cookie.match('(^|;)\\s*'+n+'\\s*=\\s*([^;]+)');return v?v.pop():'';}
async function api(u,d){let o={method:d?'POST':'GET',headers:{'Content-Type':'application/json','X-CSRFToken':gC('csrftoken')},credentials:'same-origin'};if(d)o.body=JSON.stringify(d);let r=await fetch(u,o);return{ok:r.ok,data:await r.json()}}
function show(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active');window.scrollTo(0,0)}

async function doLogin(){
let p=document.getElementById('loginPhone').value.trim();if(!p)return;
let r=await api('/api/accounts/login/',{phone:p});
if(r.ok){cU=r.data;document.getElementById('mG').textContent='Hey '+r.data.first_name+', how do you want to feel today?';if(r.data.has_profile)showMood();else show('setupScreen')}
else{let e=document.getElementById('loginError');e.style.display='block';e.textContent=r.data.error||'Login failed'}}

function pC(el){document.querySelectorAll('#cOpts .op').forEach(o=>o.classList.remove('s'));el.classList.add('s');cCo=el.dataset.v;document.getElementById('sBtn').disabled=false}
function tA(el){if(el.classList.contains('s')){el.classList.remove('s');cAn=cAn.filter(a=>a!==el.textContent)}else if(cAn.length<3){el.classList.add('s');cAn.push(el.textContent)}}
async function doSetup(){let r=await api('/api/accounts/profile/setup/',{comfort_tier:cCo,anxiety_points:cAn,interest_scores:{peace:.5,energy:.5,wonder:.5,reset:.5}});if(r.ok)showMood()}

function showMood(){cMo=cCr=cDi=null;document.querySelectorAll('.mc,.ch').forEach(e=>e.classList.remove('s'));document.getElementById('fBtn').disabled=true;
let d=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],n=new Date();
document.getElementById('mT').textContent=d[n.getDay()]+' '+n.toLocaleTimeString('en',{hour:'numeric',minute:'2-digit'});show('moodScreen')}
function pM(el,v){document.querySelectorAll('.mc').forEach(c=>c.classList.remove('s'));el.classList.add('s');cMo=v;ckM()}
function pCr(el,v){el.parentElement.querySelectorAll('.ch').forEach(c=>c.classList.remove('s'));el.classList.add('s');cCr=v;ckM()}
function pD(el,v){el.parentElement.querySelectorAll('.ch').forEach(c=>c.classList.remove('s'));el.classList.add('s');cDi=v;ckM()}
function ckM(){document.getElementById('fBtn').disabled=!(cMo&&cCr&&cDi)}

async function doFind(){show('loadScreen');let r=await api('/api/moods/find/',{mood:cMo,crowd_preference:cCr,distance:cDi});
if(r.ok&&r.data.match){cMa=r.data.match;cQI=r.data.query.id;rM(r.data);show('matchScreen')}
else{show('moodScreen');alert(r.data.message||'No matches found. Try different options.')}}

function rM(d){let m=d.match;document.getElementById('mN').textContent=m.name;document.getElementById('mA').textContent=m.area;
document.getElementById('mTags').innerHTML=(m.vibe_tags||[]).map(t=>'<span class="tag">'+t+'</span>').join('');
let i='';if(m.vibe_windows&&m.vibe_windows.length){let w=m.vibe_windows[0];i+='<p>👥 '+w.crowd_level+' crowd on '+w.day_type+'s</p>';if(w.vibe_notes)i+='<p>✨ '+w.vibe_notes+'</p>'}
if(m.match_reasons&&m.match_reasons.length)i+=m.match_reasons.map(r=>'<p>✓ '+r+'</p>').join('');
document.getElementById('mInfo').innerHTML=i||'<p>Great match for your mood.</p>';
let s='<p class="tt">🛡️ Safety info</p>';if(m.safety_intel&&m.safety_intel.length)m.safety_intel.forEach(x=>{s+='<p>'+x.content+'</p>';if(x.transport_back)s+='<p>🚗 '+x.transport_back+'</p>'});
if(m.total_visitors>0)s+='<p class="st2">'+m.total_visitors+' women visited · '+m.felt_safe_count+' felt safe</p>';
document.getElementById('mSafe').innerHTML=s;
let rv='';if(d.reviews&&d.reviews.length)d.reviews.forEach(r=>{rv+='<div class="rb"><p class="q">"'+r+'"</p><p class="at">— a woman who visited recently</p></div>'});
document.getElementById('mRevs').innerHTML=rv}

async function doR(dec,reason){let r=await api('/api/moods/respond/',{experience_id:cMa.id,mood_query_id:cQI,decision:dec,decline_reason:reason||''});
if(r.ok){cRI=r.data.id;if(dec==='going')show('goScreen');else if(dec==='skipped')doFind();else showMood()}}
function doD(el,reason){document.querySelectorAll('#decScreen .op').forEach(o=>o.classList.remove('s'));el.classList.add('s');setTimeout(()=>doR('declined',reason),300)}

function showCI(){if(cRI){document.getElementById('ciT').textContent='Did you make it to '+cMa.name+'?';document.getElementById('ci1').style.display='flex';document.getElementById('ci2').style.display='none';ciM=ciS=null;show('ciScreen')}}
function ciYes(){document.getElementById('ci1').style.display='none';document.getElementById('ci2').style.display='block';
['msR','ssR'].forEach(id=>{let c=document.getElementById(id);c.innerHTML='';[1,2,3,4,5].forEach(n=>{let b=document.createElement('button');b.className='sb2';b.textContent=n;
b.onclick=()=>{c.querySelectorAll('.sb2').forEach(x=>x.classList.remove('s'));b.classList.add('s');if(id==='msR')ciM=n;else ciS=n;document.getElementById('ciBtn').disabled=!(ciM&&ciS)};c.appendChild(b)})})}
async function doCI(){let r=await api('/api/moods/checkin/'+cRI+'/',{visited:true,visit_mood_match:ciM,visit_safety_score:ciS,visit_note:document.getElementById('ciN').value,share_review:document.getElementById('shR').checked,would_recommend:ciM>=4});
if(r.ok){document.getElementById('thxL').textContent=r.data.personality_label||'';show('thxScreen');ciM=ciS=null}}
</script>
</body>
</html>'''
write("templates/app.html", APP_HTML)

print("\n✅ All files created! Now run:")
print("   python manage.py migrate")
print("   python manage.py runserver")
print("\nThen open http://127.0.0.1:8000/ in your browser")
