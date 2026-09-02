import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class TripIntent(models.Model):
    """
    When a woman marks 'I'm going' on an experience.
    Buddy matching only triggers when she also opts in.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trip_intents")
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, related_name="trip_intents")
    intended_date = models.DateField()
    wants_buddy = models.BooleanField(default=False)  # only after explicit opt-in
    matched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "experience", "intended_date"]
        ordering = ["-created_at"]

    def __str__(self):
        buddy = " (wants buddy)" if self.wants_buddy else ""
        return f"{self.user.first_name} → {self.experience.name} on {self.intended_date}{buddy}"


class BuddyThread(models.Model):
    """
    Private thread between matched women.
    Auto-expires 48 hours after trip date.
    Max 4 women per thread.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, related_name="buddy_threads")
    trip_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Thread: {self.experience.name} on {self.trip_date}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Auto-expire 48 hours after trip date end of day
            trip_end = timezone.make_aware(
                timezone.datetime.combine(self.trip_date, timezone.datetime.max.time())
            )
            self.expires_at = trip_end + timedelta(hours=48)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at


class BuddyThreadMember(models.Model):
    """Who is in the thread — max 4 per thread."""

    thread = models.ForeignKey(BuddyThread, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buddy_memberships")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["thread", "user"]

    def __str__(self):
        return f"{self.user.first_name} in {self.thread}"


class BuddyMessage(models.Model):
    """
    Messages inside a thread.
    Deleted when thread expires. Max 500 chars.
    No links, no images — text only.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(BuddyThread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"{self.sender.first_name}: {self.content[:40]}"


class Report(models.Model):
    """
    One-tap report from inside a buddy thread.
    2+ reports from different women = auto-suspend.
    """

    REASONS = [
        ("inappropriate", "Inappropriate behavior"),
        ("not_woman", "Might not be a woman"),
        ("harassment", "Harassment"),
        ("spam", "Spam"),
        ("other", "Other"),
    ]

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports_made")
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports_received")
    thread = models.ForeignKey(BuddyThread, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=20, choices=REASONS)
    note = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["reporter", "reported_user", "thread"]

    def __str__(self):
        return f"{self.reporter.first_name} reported {self.reported_user.first_name}"
