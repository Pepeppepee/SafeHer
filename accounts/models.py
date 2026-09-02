import uuid
import secrets
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, **extra):
        user = self.model(phone=phone, first_name=first_name, **extra)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, password=None, **extra):
        user = self.model(phone=phone, first_name=first_name, is_staff=True, is_superuser=True, **extra)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Minimal user — first name and phone only.
    No last name, no photo, no age, no bio. By design.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    invited_by = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="invitees"
    )
    valley_area = models.CharField(
        max_length=20,
        choices=[
            ("kathmandu", "Kathmandu"),
            ("lalitpur", "Lalitpur / Patan"),
            ("bhaktapur", "Bhaktapur"),
            ("other", "Other valley area"),
        ],
        blank=True,
    )

    # Status
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return f"{self.first_name} ({self.phone[-4:]})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class InviteCode(models.Model):
    """
    Invite-only access. Each verified user gets 3 codes/month.
    If someone they invited gets reported, inviter loses invite ability.
    """

    code = models.CharField(max_length=8, unique=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invite_codes")
    used_by = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="used_invite"
    )
    used_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = f"used by {self.used_by}" if self.used_by else "available"
        return f"{self.code} ({status})"

    @classmethod
    def generate_code(cls):
        """Generate a unique 8-char uppercase code."""
        while True:
            code = secrets.token_hex(4).upper()
            if not cls.objects.filter(code=code).exists():
                return code


class OTPVerification(models.Model):
    """Phone OTP for login — no passwords in this app."""

    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["phone", "otp"])]

    def __str__(self):
        return f"OTP for {self.phone}"


class TravelerProfile(models.Model):
    """
    Built from onboarding quiz + updated by check-in data.
    The personality label is computed, never stored.
    """

    COMFORT_TIERS = [
        ("first_timer", "Never traveled alone"),
        ("cautious", "Cautious — been out but careful"),
        ("confident", "Confident solo traveler"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    comfort_tier = models.CharField(max_length=15, choices=COMFORT_TIERS)
    anxiety_points = models.JSONField(
        default=list,
        help_text='e.g. ["empty_streets", "men_staring", "no_signal"]',
    )
    interest_scores = models.JSONField(
        default=dict,
        help_text='e.g. {"peace": 0.9, "energy": 0.2, "wonder": 0.5}',
    )
    trips_completed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} — {self.comfort_tier}"

    @property
    def personality_label(self):
        """Derived, never stored. Changes as she grows."""
        top = max(self.interest_scores, key=self.interest_scores.get, default="peace")
        labels = {
            "peace": "Sunset Seeker",
            "energy": "Energy Chaser",
            "wonder": "Hidden Gem Finder",
            "reset": "River Soul",
            "cozy": "Cafe Wanderer",
        }
        tier_prefix = {
            "first_timer": "Budding",
            "cautious": "Growing",
            "confident": "Fearless",
        }
        return f"{tier_prefix.get(self.comfort_tier, '')} {labels.get(top, 'Explorer')}"
