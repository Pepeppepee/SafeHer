import random
from django.utils import timezone
from experiences.models import Experience, VibeWindow
from .models import MoodResponse
from datetime import datetime

COMFORT_ORDER = {"first_timer": 1, "cautious": 2, "confident": 3}
MOOD_TO_VIBES = {"peace": ["peaceful", "contemplative", "romantic"], "energy": ["energetic", "social"], "wonder": ["adventurous", "cozy"], "reset": ["peaceful", "contemplative"]}
CROWD_MAP = {"quiet": ["low"], "social": ["medium", "high"]}
# A place she's already said yes or no to today stays off the list for the rest of
# the day — regardless of what mood/vibe she asks for next. "skipped" doesn't count:
# that's just "show me another," not a real answer about the place itself.
DAY_LOCKED_DECISIONS = ["going", "declined"]

def match_experiences(profile, mood_query, limit=5):
    seen_today = MoodResponse.objects.filter(
        user=profile.user,
        decision__in=DAY_LOCKED_DECISIONS,
        recommended_at__date=timezone.localdate(),
    ).values_list("experience_id", flat=True)
    experiences = Experience.objects.filter(is_active=True).exclude(id__in=seen_today).prefetch_related("vibe_windows", "safety_intel")
    if mood_query.scene_preference:
        # A hard filter, not a scoring nudge — a mainstream landmark can out-score a hidden
        # gem on vibe-tag overlap alone (it's usually the better-documented place), so a soft
        # boost wasn't enough to stop "hidden gem" searches from still surfacing Durbar Square.
        experiences = experiences.filter(scene_type=mood_query.scene_preference)
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
        opposite_pref = "social" if mood_query.crowd_preference == "quiet" else "quiet"
        avoided_crowds = CROWD_MAP.get(opposite_pref, [])
        crowd_matched = False
        for w in windows:
            if w.crowd_level in preferred_crowds:
                score += 20
                reasons.append(f"{w.crowd_level.title()} crowd right now")
                if w.solo_comfortable:
                    score += 10
                    reasons.append("Solo comfortable")
                crowd_matched = True
                break
        if not crowd_matched:
            # A landmark can carry a "peaceful" vibe tag (its dawn kora, its quiet season)
            # while still being genuinely packed at this exact hour. Without this, asking
            # for "somewhere quiet" would still surface Durbar Square at 1pm on its tag
            # alone. Penalize — don't just fail to reward — a place that's actively in
            # the crowd state she said she doesn't want, right now.
            for w in windows:
                if w.crowd_level in avoided_crowds:
                    score -= 25
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
    # Scores tie constantly (coarse vibe/window/safety buckets), and Python's sort
    # is stable — without this, ties always resolve to whichever experience happens
    # to sit first in the queryset (e.g. newest-created), so the same place wins
    # every single time. Shuffle first so ties break differently on each query.
    random.shuffle(scored)
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]
