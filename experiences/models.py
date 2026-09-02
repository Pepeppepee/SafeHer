import uuid
from django.db import models


class Experience(models.Model):
    """
    Not a place — an experience at a place, at a time.
    "Sunset at Karya Binayak on a weekday afternoon" is the unit.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)  # "Karya Binayak sunset viewpoint"
    area = models.CharField(max_length=60)  # "Bungamati"
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Scene — how well-known/touristed this place is, not what it feels like.
    # A quiet forest temple and a packed Durbar Square can both be "contemplative";
    # this is the axis that actually separates "everyone goes here" from "almost no one does."
    SCENE_CHOICES = [
        ("mainstream", "Mainstream landmark"),
        ("hidden_gem", "Hidden gem"),
        ("cafe_social", "Café & social"),
    ]
    scene_type = models.CharField(max_length=15, choices=SCENE_CHOICES, default="hidden_gem")

    # Vibe
    VIBE_CHOICES = [
        ("peaceful", "Peaceful"),
        ("energetic", "Energetic"),
        ("romantic", "Romantic"),
        ("contemplative", "Contemplative"),
        ("social", "Social"),
        ("adventurous", "Adventurous"),
        ("cozy", "Cozy"),
    ]
    vibe_tags = models.JSONField(
        default=list,
        help_text='e.g. ["peaceful", "contemplative"]',
    )
    solo_difficulty = models.PositiveSmallIntegerField(
        help_text="1=very easy alone, 5=challenging solo",
        default=3,
    )
    min_comfort_tier = models.CharField(
        max_length=15,
        choices=[
            ("first_timer", "First timer ok"),
            ("cautious", "Cautious minimum"),
            ("confident", "Confident only"),
        ],
        default="first_timer",
    )

    # Logistics
    budget_tier = models.CharField(
        max_length=10,
        choices=[
            ("free", "Free"),
            ("under_500", "Under Rs 500"),
            ("under_1000", "Under Rs 1000"),
            ("above_1000", "Above Rs 1000"),
        ],
        default="free",
    )
    best_months = models.JSONField(default=list, blank=True, help_text="BS month numbers")

    # Aggregate safety — updated from check-in data
    total_visitors = models.PositiveIntegerField(default=0)
    felt_safe_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.area})"

    @property
    def safety_percentage(self):
        if self.total_visitors == 0:
            return None
        return round(self.felt_safe_count / self.total_visitors * 100)


class VibeWindow(models.Model):
    """
    Same place, different times = different experience.
    Swayambhu at 6am is peace; at noon it's chaos.
    """

    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="vibe_windows")
    day_type = models.CharField(
        max_length=10,
        choices=[
            ("weekday", "Weekday"),
            ("weekend", "Weekend"),
            ("any", "Any day"),
        ],
    )
    time_start = models.TimeField(help_text="e.g. 16:00")
    time_end = models.TimeField(help_text="e.g. 19:00")
    crowd_level = models.CharField(
        max_length=10,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
    )
    vibe_notes = models.CharField(max_length=200, blank=True)  # "calm, golden light, few families"
    solo_comfortable = models.BooleanField(
        default=True,
        help_text="Can a woman sit alone here without stares?",
    )

    class Meta:
        ordering = ["day_type", "time_start"]

    def __str__(self):
        return f"{self.experience.name} — {self.day_type} {self.time_start}-{self.time_end}"


class SafetyIntel(models.Model):
    """
    Structured safety data — your moat.
    One place can have multiple safety entries by category.
    """

    CATEGORIES = [
        ("transport", "Transport"),
        ("accommodation", "Accommodation"),
        ("area_safety", "Area at night"),
        ("connectivity", "Connectivity"),
        ("local_attitude", "Local attitude"),
        ("emergency", "Emergencies"),
        ("return_route", "Getting back"),
    ]
    SOURCE_TYPES = [
        ("founder_verified", "Founder verified"),
        ("community", "Community report"),
        ("partner", "Partner verified"),
    ]

    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="safety_intel")
    category = models.CharField(max_length=20, choices=CATEGORIES)
    content = models.TextField()  # "Pathao available till ~8pm, less reliable after"
    safe_until = models.TimeField(
        null=True, blank=True,
        help_text="Last comfortable time to be here",
    )
    transport_back = models.CharField(
        max_length=200, blank=True,
        help_text="How to get back + cutoff time",
    )
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, default="founder_verified")
    verified_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category"]

    def __str__(self):
        return f"{self.experience.name} — {self.category}"


class VerifiedStay(models.Model):
    """Solo-woman-friendly accommodations/cafes near an experience."""

    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="verified_stays")
    name = models.CharField(max_length=100)
    stay_type = models.CharField(
        max_length=15,
        choices=[
            ("homestay", "Homestay"),
            ("hotel", "Hotel"),
            ("cafe", "Café"),
            ("restaurant", "Restaurant"),
        ],
    )
    # 60, not 30: this is free text like "Rs 1,500-3,000/night incl. meals", which
    # already overflowed 30. SQLite ignores max_length so it only surfaced on Postgres.
    price_range = models.CharField(max_length=60, blank=True)
    verification_note = models.TextField(blank=True)  # "Owner is a woman, has hosted solo travelers"
    contact = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} near {self.experience.name}"
