import uuid
from django.db import models
from django.conf import settings


class MoodQuery(models.Model):
    """
    What she asked for — mood + modifiers.
    One per session. Drives the recommendation.
    """

    MOOD_CHOICES = [
        ("peace", "Peace"),
        ("energy", "Energy"),
        ("wonder", "Wonder"),
        ("reset", "Reset"),
    ]
    CROWD_CHOICES = [
        ("quiet", "Somewhere quiet"),
        ("social", "Around people"),
    ]
    DISTANCE_CHOICES = [
        ("walkable", "Walkable"),
        ("under_1hr", "Under 1 hour"),
        ("day_trip", "Day trip"),
    ]
    # Mirrors Experience.SCENE_CHOICES — what kind of place she's actually looking for,
    # not just what mood/crowd. Without this, matching falls back to whichever place has
    # the strongest vibe-tag overlap, which skews mainstream since those are best-documented.
    SCENE_CHOICES = [
        ("mainstream", "Mainstream landmark"),
        ("hidden_gem", "Hidden gem"),
        ("cafe_social", "Café & social"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mood_queries")
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    crowd_preference = models.CharField(max_length=10, choices=CROWD_CHOICES)
    distance = models.CharField(max_length=10, choices=DISTANCE_CHOICES)
    scene_preference = models.CharField(max_length=15, choices=SCENE_CHOICES, default="hidden_gem")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "mood queries"

    def __str__(self):
        return f"{self.user.first_name} — {self.mood} / {self.crowd_preference}"


class MoodResponse(models.Model):
    """
    One row per recommendation shown.
    Feeds: place data correction, profile evolution, reviews.
    This table IS the data flywheel.
    """

    DECISION_CHOICES = [
        ("going", "I'm going"),
        ("declined", "Not this time"),
        ("skipped", "Show another"),
    ]
    DECLINE_REASONS = [
        ("wrong_mood", "Wrong mood"),
        ("too_far", "Too far"),
        ("not_safe", "Doesn't feel safe"),
        ("been_there", "Already been"),
        ("bad_timing", "Bad timing"),
        ("other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mood_responses")
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, related_name="mood_responses")
    mood_query = models.ForeignKey(MoodQuery, on_delete=models.CASCADE, related_name="responses")

    # Decision
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES)
    decline_reason = models.CharField(max_length=15, choices=DECLINE_REASONS, blank=True)
    decline_note = models.CharField(max_length=200, blank=True)

    # Check-in (filled later)
    visited = models.BooleanField(null=True)  # null = not checked in yet
    visit_mood_match = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="1-5: did it deliver the feeling she wanted?",
    )
    visit_safety_score = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="1-5: how safe did she feel?",
    )
    visit_note = models.TextField(blank=True)  # richest signal — free text
    would_recommend = models.BooleanField(null=True)
    share_review = models.BooleanField(
        default=False,
        help_text="Did she opt to share her note anonymously with other women?",
    )

    recommended_at = models.DateTimeField(auto_now_add=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-recommended_at"]

    def __str__(self):
        return f"{self.user.first_name} → {self.experience.name} ({self.decision})"
