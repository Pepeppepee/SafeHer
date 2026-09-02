# SafeHer — Mood-to-Experience Travel App

> "Tell me your mood today, and I'll show you where in the valley to go feel it — safely, as a woman."

## Quick start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # settings read the environment; see the file for what to fill in
python manage.py migrate
python manage.py seed_valley_places
python manage.py createsuperuser
python manage.py runserver
```

Admin panel: http://localhost:8000/admin/

Deploying to Render: see [DEPLOY.md](DEPLOY.md).

## Project structure

```
safeher/             — Django project settings
accounts/            — User, InviteCode, OTP, TravelerProfile
  models.py          — Minimal user (first name + phone only, by design)
experiences/         — Experience, VibeWindow, SafetyIntel, VerifiedStay
  models.py          — The destination data with time-based vibe windows
moods/               — MoodQuery, MoodResponse
  models.py          — The data flywheel (recommendations + check-ins)
  matcher.py         — Mood-to-experience matching engine (no ML)
buddies/             — TripIntent, BuddyThread, BuddyMessage, Report
  models.py          — Blind buddy matching with auto-expiry
```

## Apps overview

### accounts
- Invite-only signup (no public registration)
- Phone OTP auth (no passwords)
- TravelerProfile with comfort tier + anxiety points
- Personality label is computed, never stored

### experiences
- Experience = a vibe at a place at a time (not just a location)
- VibeWindow = same place, different time = different experience
- SafetyIntel = structured safety data per category
- VerifiedStay = solo-woman-friendly accommodations

### moods
- MoodQuery = what she asked for (mood + crowd + distance)
- MoodResponse = decision + check-in (the entire feedback loop)
- matcher.py = weighted scoring, no ML, transparent and debuggable

### buddies
- TripIntent = "I'm going" with optional buddy opt-in
- BuddyThread = private, expires 48hr after trip, max 4 women
- Report = one-tap, 2 reports = auto-suspend

## Security rules
- No last names, photos, ages, or bios collected
- Place pages show only anonymous aggregate counts
- Buddy matching is blind until mutual opt-in
- Thread auto-expires 48 hours after trip date
- Rate limits: max 3 intents/week, 2 active threads
