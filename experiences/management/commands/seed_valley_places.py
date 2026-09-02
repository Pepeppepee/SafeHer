"""
Seeds Experience/VibeWindow/SafetyIntel/VerifiedStay with real, researched
places across Kathmandu Valley (Kathmandu, Lalitpur, Bhaktapur districts only).

Idempotent — safe to re-run. Matches on (name, area).

    python manage.py seed_valley_places
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from experiences.models import Experience, VibeWindow, SafetyIntel, VerifiedStay

VERIFIED_DATE = "2026-08-29"

PLACES = [
    {
        "name": "Garden of Dreams",
        "area": "Thamel, Kathmandu",
        "description": (
            "A walled neoclassical garden right off Thamel's chaos — fountains, pergolas, a café lawn. "
            "Correction from an earlier version of this data: this is NOT a quiet solitude spot — it's "
            "widely known as Kathmandu's most popular dating and pre-wedding photoshoot location, and "
            "gets genuinely crowded with couples and photo shoots, especially afternoons and weekends. "
            "Go right at opening on a weekday if you actually want it calm."
        ),
        "latitude": "27.714900", "longitude": "85.313800",
        "vibe_tags": ["romantic", "cozy", "social"],
        "solo_difficulty": 2,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_500",
        "scene_type": "mainstream",
        "windows": [
            dict(day_type="weekday", time_start="09:00", time_end="11:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Calmest window it gets — gates just opened, before the photoshoot crowd arrives"),
            dict(day_type="any", time_start="11:00", time_end="19:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Kathmandu's #1 dating and pre-wedding photoshoot spot — couples, photographers, groups"),
            dict(day_type="weekend", time_start="09:00", time_end="19:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Busiest window of the week — go on a weekday instead if crowds bother you"),
        ],
        "safety": [
            dict(category="transport",
                 content="Walkable from any Thamel hotel (5–10 min). Pathao/inDrive/Tootle bike or car "
                         "all serve Thamel reliably till late; fare in-app is fixed with Pathao, negotiable on inDrive.",
                 source_type="founder_verified"),
            dict(category="area_safety",
                 content="Inside a locked, staffed compound — the safest sit-alone spot in central Kathmandu. "
                         "Thamel's surrounding lanes are well lit and busy with tourists/shops till ~10pm.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Full 4G/5G, plus free wifi at the in-garden Kaiser Café."),
            dict(category="local_attitude",
                 content="Extremely tourist-habituated; staff and vendors are used to solo foreign and Nepali women. "
                         "Ignore the odd tout at the gate — a firm 'no' works."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 (call/SMS, 24/7) · Ambulance 102. "
                         "Tourist Police booth is a 5-min walk at Thamel Chowk."),
            dict(category="return_route",
                 content="Gates close 8pm sharp. Book your ride out via app before then — queuing a street taxi "
                         "after dark in Thamel is the one part locals don't recommend for a first-timer.",
                 transport_back="Pathao/inDrive car back to hotel; walk only if your stay is inside Thamel itself.",
                 safe_until="20:00"),
        ],
        "stays": [
            dict(name="Kathmandu Guest House (KGH)", stay_type="hotel", price_range="Rs 3,500–8,000/night",
                 verification_note="Landmark heritage hotel since 1968, walled compound, 24hr front desk, "
                                    "long track record hosting solo women travelers."),
            dict(name="Rest Up Kathmandu Hostel", stay_type="homestay", price_range="Rs 800–1,500/night (dorm)",
                 verification_note="Female-only dorms with lockers, quiet side-street location a few minutes from Thamel's main strip."),
            dict(name="Kaiser Café (inside the garden)", stay_type="cafe", price_range="Rs 300–700/item",
                 verification_note="In-garden café, staffed till closing, popular solo work/reading spot."),
        ],
    },
    {
        "name": "Patan Durbar Square & Museum",
        "area": "Patan, Lalitpur",
        "description": (
            "Newar royal square across the river from Kathmandu — a working UNESCO heritage site, not "
            "a quiet retreat. It's genuinely busy from late morning through the afternoon (tour groups, "
            "vendors, photographers); the only real calm window is right at opening. Patan Museum inside "
            "the old palace is a legitimately quiet indoor option once the square itself fills up."
        ),
        "latitude": "27.672700", "longitude": "85.324700",
        "vibe_tags": ["contemplative", "social"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "mainstream",
        "windows": [
            dict(day_type="any", time_start="07:00", time_end="09:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="The one genuinely quiet window — locals doing morning puja, soft light, square just waking up"),
            dict(day_type="any", time_start="11:00", time_end="15:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Peak tour-group and midday-heat window — avoid if you want it calm"),
            dict(day_type="weekend", time_start="16:00", time_end="19:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Families out in the square, street food stalls, lively but not rowdy"),
        ],
        "safety": [
            dict(category="transport",
                 content="15–25 min / Rs 300–500 by Pathao or inDrive car from Thamel or Kathmandu Durbar Square. "
                         "Local bus/tempo from Ratna Park also runs but is a stand-and-squeeze ride — car apps are easier solo."),
            dict(category="area_safety",
                 content="Ticketed core square has guards; the surrounding old-town lanes (Mangal Bazaar) are safe "
                         "and busy through early evening. Gets noticeably quieter after 8pm.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Good 4G throughout; museum and cafés around the square have wifi."),
            dict(category="local_attitude",
                 content="Quieter, less touristy than Thamel — locals are polite and mostly indifferent to solo women, "
                         "which many first-timers find more comfortable than Kathmandu's tourist core."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Police post is on the square itself, next to the museum entrance."),
            dict(category="return_route",
                 content="Pre-book your return car before sunset in winter (dark by ~5:30pm Nov–Jan) since Patan's "
                         "side streets are dim at night even though they're safe.",
                 transport_back="Pathao/inDrive car directly to your hotel — cheap and a fixed 15–25 min.",
                 safe_until="19:00"),
        ],
        "stays": [
            dict(name="Café du Temple", stay_type="cafe", price_range="Rs 400–900/item",
                 verification_note="Rooftop café overlooking the square, popular solo perch, staffed all day."),
            dict(name="Boutique heritage guesthouses, Mangal Bazaar", stay_type="homestay", price_range="Rs 2,500–5,000/night",
                 verification_note="Small family-run heritage stays in the old town — quieter than Thamel, "
                                    "repeatedly recommended by solo female travelers for the peaceful neighbourhood."),
        ],
    },
    {
        "name": "Boudhanath Stupa — dawn kora",
        "area": "Boudha, Kathmandu",
        "description": (
            "The valley's biggest stupa, ringed by monasteries and Tibetan restaurants. Correction from "
            "an earlier version of this data: 4–6pm is actually the single busiest window here — tour "
            "buses run 10am–2pm and the plaza is a packed 'human roundabout' by evening golden hour, not "
            "the calm moment it sounds like. The real quiet kora is at dawn, or after 7pm once the "
            "butter lamps are lit and the tour groups have left."
        ),
        "latitude": "27.721500", "longitude": "85.362000",
        "vibe_tags": ["peaceful", "social", "contemplative"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_500",
        "scene_type": "mainstream",
        "windows": [
            dict(day_type="any", time_start="05:30", time_end="07:30",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Quiet dawn kora with elderly locals and monks, cafés just opening — the genuinely peaceful window"),
            dict(day_type="any", time_start="10:00", time_end="14:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Tour-bus peak, hawkers most persistent — fine to visit, just not calm"),
            dict(day_type="any", time_start="16:00", time_end="18:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="The busiest window of the day despite the golden light — a packed 'human roundabout'"),
            dict(day_type="any", time_start="19:00", time_end="21:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Butter lamps lit, tour groups gone, contemplative without being empty"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–700 by Pathao/inDrive from Thamel; also reachable by local bus from Ratna Park "
                         "(look for 'Boudha' buses, Rs 25–30) but a car is far less hassle with no local-language signage."),
            dict(category="area_safety",
                 content="The stupa plaza is bright, camera-covered, and busy with restaurant lights until ~9–10pm. "
                         "The narrow lanes leading away from the plaza get dark and empty faster.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Reliable 4G; most rooftop cafés around the stupa have wifi."),
            dict(category="local_attitude",
                 content="Calm, monastery-adjacent neighbourhood; large resident Tibetan community, very used to "
                         "solo travelers doing the kora at all hours."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "A police box sits at the main east gate to the stupa."),
            dict(category="return_route",
                 content="Book your ride out from right at the stupa gate (strong GPS signal, well lit) rather than "
                         "walking into the side lanes to hail one.",
                 transport_back="Pathao/inDrive car back to Thamel or central Kathmandu, ~20–30 min.",
                 safe_until="21:00"),
        ],
        "stays": [
            dict(name="Rosebud Café / Stupa View rooftop cafés", stay_type="cafe", price_range="Rs 400–1,000/item",
                 verification_note="Rooftop cafés directly overlooking the stupa, staffed and busy through the evening kora hours."),
            dict(name="Boudha-area guesthouses", stay_type="hotel", price_range="Rs 2,000–4,500/night",
                 verification_note="Small hotels within the kora circuit — waking up to the 6am kora is a common solo-traveler draw."),
        ],
    },
    {
        # Added after correcting the false "peaceful" tags on Garden of Dreams/Patan/Bhaktapur/
        # Boudhanath — a genuinely quiet, low-crowd Tibetan Buddhist monastery to actually
        # back up the "peace" mood with real solitude rather than a busy landmark.
        "name": "Kopan Monastery",
        "area": "Kopan, Kathmandu",
        "description": (
            "A working Tibetan Buddhist monastery on a quiet hillside above Boudha — meditation gardens, "
            "monks' morning prayers, and a real valley view without a single tour bus. Genuinely one of "
            "the few places in the valley that's peaceful by default rather than only at one narrow hour."
        ),
        "latitude": "27.735000", "longitude": "85.362000",
        "vibe_tags": ["peaceful", "contemplative"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="07:00", time_end="11:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Monks' morning prayers, gardens near-empty, genuinely tranquil rather than just quiet-for-Kathmandu"),
            dict(day_type="any", time_start="13:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Office reopens 1pm, still very few visitors outside of course participants"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from Thamel via Boudha, or walk up the hill "
                         "from Boudhanath (steep, ~25 min) if you're already there. Local buses from Ratna Park "
                         "toward Boudha exist but don't go all the way up — you'd still walk the last stretch."),
            dict(category="area_safety",
                 content="Calm monastery grounds with monks and staff around all day. Gate closes at 5pm sharp — "
                         "day visits are also suspended during long retreat courses (typically Nov–Dec), so it's "
                         "worth checking ahead rather than showing up unannounced.",
                 safe_until="16:30"),
            dict(category="connectivity", content="Patchy 4G on the hill road up, weak but present inside the monastery grounds."),
            dict(category="local_attitude",
                 content="Welcoming to respectful visitors — dress modestly (cover shoulders and knees), remove "
                         "shoes before prayer halls, and keep your voice down near the gompa during chanting."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Monastery office staff can also assist directly during opening hours."),
            dict(category="return_route",
                 content="Leave enough time to be down the hill before the 5pm gate closure — signal is weak up "
                         "here, so arrange your ride while you still have a bar of signal near the office.",
                 transport_back="Pathao/inDrive car back toward Boudha/Thamel, ~30–40 min.",
                 safe_until="16:30"),
        ],
        "stays": [],
    },
    {
        "name": "Swayambhunath sunrise",
        "area": "Swayambhu, Kathmandu",
        "description": (
            "The 'Monkey Temple' hilltop stupa with the best panoramic view of the whole valley. "
            "Go at sunrise before the tour buses and the monkeys get bold — same place is chaos by noon."
        ),
        "latitude": "27.714900", "longitude": "85.290300",
        "vibe_tags": ["peaceful", "contemplative", "adventurous"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_500",
        "scene_type": "mainstream",
        "windows": [
            dict(day_type="any", time_start="05:30", time_end="07:30",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Locals doing morning parikrama, valley view clear before haze builds, few tourists"),
            dict(day_type="any", time_start="11:00", time_end="16:00",
                 crowd_level="high", solo_comfortable=False,
                 vibe_notes="Tour-bus peak, aggressive monkeys around food stalls, best avoided solo"),
        ],
        "safety": [
            dict(category="transport",
                 content="10–15 min / Rs 250–400 by Pathao/inDrive from Thamel to the eastern stairway (365 steps) "
                         "or the western vehicle gate. For a sunrise visit, book the ride the night before — "
                         "very few drivers are online online pre-5:30am."),
            dict(category="area_safety",
                 content="Hilltop plaza is open and has resident monks/vendors from dawn; the long stone stairway "
                         "up is unlit and quiet before sunrise — go with the steady trickle of local walkers, not first alone in the dark.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Patchy 4G on the stairway itself, full signal at the top plaza."),
            dict(category="local_attitude",
                 content="Mixed: monks and long-time vendors are welcoming; be firm and keep bags zipped near the "
                         "monkeys, who grab food and shiny objects, not a safety issue re: people."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "A police post sits at the base of the eastern stairway."),
            dict(category="return_route",
                 content="Have your ride pick you up from the western gate car park (not the stairway base) — "
                         "it's better lit and has steadier phone signal for the app to locate you.",
                 transport_back="Pathao/inDrive car back down to Kathmandu; walking down after dark is not recommended solo.",
                 safe_until="19:00"),
        ],
        "stays": [
            dict(name="Stupa View Restaurant (western gate)", stay_type="restaurant", price_range="Rs 300–700/item",
                 verification_note="Breakfast spot right at the vehicle gate, good place to wait for your ride after sunrise."),
        ],
    },
    {
        "name": "Karya Binayak sunset viewpoint, Bungamati",
        "area": "Bungamati, Lalitpur",
        "description": (
            "A red-brick Newar farming village on the valley's southern edge, barely touched by tourism. "
            "The Karya Binayak temple grove above the village catches sunset over terraced fields — "
            "wood-carving workshops and courtyard life fill the lanes below."
        ),
        "latitude": "27.642000", "longitude": "85.305000",
        "vibe_tags": ["peaceful", "cozy"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="15:30", time_end="18:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Farmers heading home, kids playing in courtyards, calm golden light on the temple grove"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from central Kathmandu (Ring Road south to Bungamati). "
                         "No reliable local bus for a solo day trip — book a car both ways rather than trying to combine with local transit."),
            dict(category="area_safety",
                 content="Very low crime, small-village feel with constant foot traffic from residents; the temple "
                         "grove itself is quiet and semi-isolated after dusk.",
                 safe_until="18:00"),
            dict(category="connectivity", content="Basic 4G, can drop to 3G in the temple grove — not a place to rely on live navigation."),
            dict(category="local_attitude",
                 content="Genuinely welcoming, low tourist volume means more curiosity than hassle; woodcarving "
                         "workshop owners are used to a handful of visitors and happy to chat."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Nearest police post is in Bungamati village center, ~5 min from the temple grove."),
            dict(category="return_route",
                 content="Signal is weak enough near the grove that app-hailing can be slow — request your return "
                         "ride from the village center before walking up, and confirm the driver has the pin.",
                 transport_back="Pre-booked Pathao/inDrive car back to Kathmandu; do not plan to flag a ride here after dark.",
                 safe_until="18:00"),
        ],
        "stays": [
            dict(name="Bungamati homestays", stay_type="homestay", price_range="Rs 1,500–3,000/night incl. meals",
                 verification_note="Family-run village homestays; several hosted by women, meals eaten with the household — "
                                    "book ahead, capacity is small."),
        ],
    },
    {
        "name": "Kirtipur old town walk",
        "area": "Kirtipur, Kathmandu",
        "description": (
            "A hilltop Newar town predating Kathmandu itself — narrow brick lanes, weaving looms in "
            "doorways, two hilltop temples with valley views, and Tribhuvan University's campus at its foot."
        ),
        "latitude": "27.677400", "longitude": "85.277700",
        "vibe_tags": ["contemplative", "peaceful"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="weekday", time_start="09:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Students around the university gate, weavers working, quiet temple courtyards"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–600 by Pathao/inDrive from Thamel or New Road; local buses to "
                         "Kirtipur/Tribhuvan University run from Ratna Park for Rs 20–30 if you want the local experience."),
            dict(category="area_safety",
                 content="Safe, low-key university-town feel through the afternoon; the old-town lanes above the "
                         "campus thin out noticeably by early evening.",
                 safe_until="17:30"),
            dict(category="connectivity", content="Good 4G on the main road, patchier in the oldest upper lanes."),
            dict(category="local_attitude",
                 content="Student and academic community, generally respectful toward solo women; far less "
                         "tourist-facing than Thamel so expect curiosity rather than sales pitches."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your return ride from near the university gate at the base of the hill — better "
                         "signal and easier for a driver to find than the upper old-town lanes.",
                 transport_back="Pathao/inDrive car back to Kathmandu, ~20–30 min.",
                 safe_until="17:30"),
        ],
        "stays": [
            dict(name="Newari Kitchen, Kirtipur", stay_type="restaurant", price_range="Rs 300–600/meal",
                 verification_note="Local Newar thali spot near the university, family-run, good midday stop."),
        ],
    },
    {
        "name": "Taudaha Lake",
        "area": "Taudaha, Kathmandu",
        "description": (
            "A quiet natural lake on the valley's southern rim, ringed by fields and a birding trail. "
            "Legend says it's the drained-out serpent lake of the valley's creation myth — today it's "
            "migratory birds, paddle boats, and a handful of lakeside tea stalls."
        ),
        "latitude": "27.657700", "longitude": "85.287400",
        "vibe_tags": ["peaceful", "romantic"],
        "solo_difficulty": 3,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_500",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="07:00", time_end="10:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Best birdwatching light, misty water, a few local fishermen and walkers"),
            dict(day_type="weekend", time_start="10:00", time_end="16:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Families with paddle boats, tea stalls open, more foot traffic around the lake path"),
        ],
        "safety": [
            dict(category="transport",
                 content="25–35 min / Rs 500–800 by Pathao/inDrive from central Kathmandu. No practical public "
                         "transit for a solo trip — book a car and ideally have it wait or arrange a pickup time."),
            dict(category="area_safety",
                 content="Open countryside with scattered visitors rather than a crowd — fine mid-morning to "
                         "afternoon, but isolated enough that going at dawn or alone after 4pm isn't advised.",
                 safe_until="16:30"),
            dict(category="connectivity", content="Patchy 3G/4G around the lake — tell someone your plan before you go, "
                                                    "don't rely on live location sharing here."),
            dict(category="local_attitude", content="Local farmers and tea-stall owners, low tourist traffic; polite but not used to solo foreign women — "
                                                      "expect stares more than hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Nearest police post is on the Kathmandu–Dakshinkali road, a short ride away."),
            dict(category="return_route",
                 content="Weak signal near the lake makes on-the-spot ride-hailing unreliable — pre-arrange your "
                         "pickup time and location with the driver before you're dropped off.",
                 transport_back="Pre-booked Pathao/inDrive car; do not plan to hail one at the lakeside.",
                 safe_until="16:30"),
        ],
        "stays": [
            dict(name="Lakeside tea stalls", stay_type="cafe", price_range="Rs 100–300/item",
                 verification_note="Simple family-run tea and noodle stalls along the lake path, open daytime only."),
        ],
    },
    {
        "name": "Shivapuri Nagarjun day hike",
        "area": "Budhanilkantha, Kathmandu",
        "description": (
            "The valley's forested northern wall — a national park with a graded trail to Shivapuri "
            "peak (2,732m) through pine and oak forest, langurs, and a couple of monasteries en route. "
            "A full but manageable day hike, best with at least one other person."
        ),
        "latitude": "27.783300", "longitude": "85.366700",
        "vibe_tags": ["adventurous", "peaceful"],
        "solo_difficulty": 4,
        "min_comfort_tier": "confident",
        "budget_tier": "under_500",
        "scene_type": "hidden_gem",
        "best_months": [6, 7, 8, 12, 1],
        "windows": [
            dict(day_type="any", time_start="07:00", time_end="15:00",
                 crowd_level="low", solo_comfortable=False,
                 vibe_notes="Forested trail, other hikers thin out fast past the entrance gate — go with a buddy, not solo"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–1,000 by Pathao/inDrive from Thamel to the Panimuhan/Sundarijal entrance gate. "
                         "Local bus to Sundarijal exists (Rs 30–40 from Ratna Park) but adds significant time."),
            dict(category="area_safety",
                 content="National park entrance is staffed and ticketed, but the upper trail is remote forest with "
                         "long stretches of no other people — this is the one experience in the valley we don't "
                         "recommend solo regardless of comfort tier. Use the app's buddy match.",
                 safe_until="15:00"),
            dict(category="connectivity", content="No signal for long stretches above the entrance gate — tell someone "
                                                    "your route and expected return time before you start."),
            dict(category="local_attitude", content="Park rangers and monastery staff are helpful; you're unlikely to "
                                                      "meet many people at all on the upper trail on a weekday."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Park entrance office has a ranger station — sign the trail register on the way in."),
            dict(category="return_route",
                 content="Aim to be back at the entrance gate by 3pm — the forest loses light fast and signal for a "
                         "ride-hail app returns only once you're back near the gate.",
                 transport_back="Pathao/inDrive car from the entrance gate back to Kathmandu, ~30–40 min.",
                 safe_until="15:30"),
        ],
        "stays": [
            dict(name="Park entrance tea shop", stay_type="cafe", price_range="Rs 100–300/item",
                 verification_note="Simple shop at the gate for pre/post-hike tea, staffed during park hours."),
        ],
    },
    {
        "name": "Champadevi hill hike",
        "area": "Pharping, Kathmandu",
        "description": (
            "A half-day ridge hike on the valley's southern rim (2,285m) starting near Pharping's "
            "Tibetan monasteries, with a 360° view of the valley and the Himalaya on a clear day."
        ),
        "latitude": "27.616700", "longitude": "85.283300",
        "vibe_tags": ["adventurous", "peaceful"],
        "solo_difficulty": 4,
        "min_comfort_tier": "confident",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "best_months": [6, 7, 8, 12, 1],
        "windows": [
            dict(day_type="any", time_start="07:00", time_end="13:00",
                 crowd_level="low", solo_comfortable=False,
                 vibe_notes="Forest trail past monasteries, quiet ridge at the top — go with a buddy or small group"),
        ],
        "safety": [
            dict(category="transport",
                 content="40–50 min / Rs 800–1,200 by Pathao/inDrive from Kathmandu to Pharping trailhead. "
                         "No practical public transit for a same-day solo hike."),
            dict(category="area_safety",
                 content="Trail passes active monasteries (people around at the start) but thins to empty forest "
                         "ridge for most of the climb — pair up via the app's buddy feature rather than going alone.",
                 safe_until="14:00"),
            dict(category="connectivity", content="No signal on most of the ridge trail; share your route before you start."),
            dict(category="local_attitude", content="Monastery communities at the base are welcoming and accustomed to visitors."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Pharping has a small police post near the main monastery cluster."),
            dict(category="return_route",
                 content="Signal only returns once you're back down near the monasteries — request your ride from "
                         "there rather than expecting connectivity on the ridge.",
                 transport_back="Pathao/inDrive car from Pharping back to Kathmandu, ~40–50 min.",
                 safe_until="15:00"),
        ],
        "stays": [
            dict(name="Pharping monastery guesthouses", stay_type="homestay", price_range="Rs 1,000–2,500/night",
                 verification_note="Simple guesthouses attached to the monastery complex, quiet and family-run."),
        ],
    },
    {
        "name": "Chandragiri Hills cable car viewpoint",
        "area": "Thankot, Kathmandu",
        "description": (
            "A 10-minute cable car ride up the valley's western rim (2,551m) to a Himalayan viewpoint, "
            "temple, and a couple of view-restaurants — the easiest 'mountain view' in the valley since "
            "you don't have to hike to get it."
        ),
        "latitude": "27.665000", "longitude": "85.224200",
        "vibe_tags": ["adventurous", "romantic"],
        "solo_difficulty": 2,
        "min_comfort_tier": "first_timer",
        "budget_tier": "above_1000",
        "scene_type": "mainstream",
        "windows": [
            dict(day_type="any", time_start="08:00", time_end="16:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Cable car queues and view-restaurant crowd, family day-trip atmosphere, staffed throughout"),
        ],
        "safety": [
            dict(category="transport",
                 content="35–45 min / Rs 700–1,100 by Pathao/inDrive from Thamel to the cable car base station. "
                         "Cable car ticket (~Rs 900 round trip for foreigners, cheaper for Nepali citizens) covers the ride up and down."),
            dict(category="area_safety",
                 content="Fully commercial tourist operation — staffed cable car, ticket counters, guarded viewpoint "
                         "plaza. One of the lowest-risk 'adventure' outings in the valley for a first-timer.",
                 safe_until="16:30"),
            dict(category="connectivity", content="Good signal at both base and summit stations."),
            dict(category="local_attitude", content="Tourism-staff professional and used to solo visitors, domestic and foreign."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Cable car staff and on-site management can assist directly at either station."),
            dict(category="return_route",
                 content="Last cable car down is typically mid-afternoon to early evening — confirm the day's last "
                         "descent time at the ticket counter when you go up.",
                 transport_back="Cable car down, then pre-booked Pathao/inDrive car from the base station back to Kathmandu.",
                 safe_until="17:00"),
        ],
        "stays": [
            dict(name="Chandragiri Hills view restaurant", stay_type="restaurant", price_range="Rs 500–1,200/meal",
                 verification_note="On-site restaurant at the summit station, staffed daily during operating hours."),
        ],
    },
    {
        "name": "Bhaktapur Durbar Square day trip",
        "area": "Bhaktapur",
        "description": (
            "The best-preserved of the valley's three royal cities — pottery square, Nyatapola temple, "
            "pedestrianized brick lanes. Less touristy than Kathmandu's own Durbar Square, but still a "
            "major UNESCO landmark that fills up with tour groups by mid-morning and locals on weekends — "
            "the calm, almost-peaceful version of it only really exists early morning or after 4pm."
        ),
        "latitude": "27.672200", "longitude": "85.427800",
        "vibe_tags": ["contemplative", "social"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "mainstream",
        "windows": [
            dict(day_type="any", time_start="06:00", time_end="09:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Genuinely quiet, almost peaceful — potters setting up in Pottery Square, temple courtyards empty"),
            dict(day_type="weekday", time_start="09:00", time_end="16:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Tour groups through the main square, still easy solo wandering in side lanes"),
            dict(day_type="weekend", time_start="10:00", time_end="18:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Domestic tourists and families out, street-food stalls busy, still low-hassle"),
        ],
        "safety": [
            dict(category="transport",
                 content="35–45 min / Rs 700–1,000 by Pathao/inDrive from Thamel or Kathmandu Durbar Square, or "
                         "the Sajha/local bus from Ratna Park (Rs 30–40, slower). The old town itself is pedestrian-only."),
            dict(category="area_safety",
                 content="Pedestrianized core with constant local foot traffic and a visible police presence near "
                         "the main squares through the evening.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Good 4G throughout the old town."),
            dict(category="local_attitude",
                 content="Calm, proud-of-their-heritage community, low hassle for solo women; craft-shop and café "
                         "owners are friendly without being pushy."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Tourist-facing police post near Durbar Square's main ticket gate."),
            dict(category="return_route",
                 content="Order your car from one of the main squares (strong signal, well lit, easy for a driver "
                         "to find) rather than a back lane.",
                 transport_back="Pathao/inDrive car back to Kathmandu, ~35–45 min.",
                 safe_until="20:00"),
        ],
        "stays": [
            dict(name="Old-town heritage guesthouses", stay_type="hotel", price_range="Rs 2,000–5,000/night",
                 verification_note="Several small heritage hotels inside the pedestrianized core — waking up inside "
                                    "Durbar Square before the day-trippers arrive is the main draw."),
            dict(name="Café Nyatapola", stay_type="cafe", price_range="Rs 300–800/item",
                 verification_note="Multi-floor café built into a traditional building overlooking Taumadhi Square, staffed all day."),
        ],
    },
    {
        "name": "Nagarkot sunrise viewpoint",
        "area": "Nagarkot, Bhaktapur",
        "description": (
            "A ridge village on the valley's eastern rim (2,175m), the valley's classic sunrise-over-the-"
            "Himalaya spot on a clear day. Best done as an overnight so you're already there at dawn, "
            "rather than a rushed pre-sunrise drive up."
        ),
        "latitude": "27.717200", "longitude": "85.520100",
        "vibe_tags": ["peaceful", "romantic", "adventurous"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_1000",
        "scene_type": "mainstream",
        "best_months": [6, 7, 8, 12, 1],
        "windows": [
            dict(day_type="any", time_start="05:30", time_end="07:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="View-tower crowd for sunrise, mostly other travelers and a few guides — friendly, not isolating"),
            dict(day_type="any", time_start="16:00", time_end="18:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Quiet ridge walks between guesthouses, terraced-hill views, sunset lower-key than sunrise"),
        ],
        "safety": [
            dict(category="transport",
                 content="1–1.5 hr / Rs 1,500–2,500 by Pathao/inDrive from Kathmandu (winding hill road). Shared "
                         "jeeps also run from Bhaktapur for a cheaper but slower option. Booking a private car for "
                         "an overnight is the least stressful option solo."),
            dict(category="area_safety",
                 content="Small guesthouse-strip village geared entirely around sunrise tourism — safe and quiet, "
                         "but genuinely rural with no streetlights between properties after dark.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Decent 4G in the village center, weaker at some outlying resorts — "
                                                    "confirm your guesthouse's signal before booking if you need to stay connected."),
            dict(category="local_attitude", content="Entirely used to independent travelers of all kinds; guesthouse "
                                                      "owners are a good source of same-morning sunrise-buddy company."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Nagarkot has a small police post on the main ridge road."),
            dict(category="return_route",
                 content="Bring a flashlight for the short guesthouse-to-viewtower walk pre-dawn — no streetlighting "
                         "on the ridge. Book your car back to Kathmandu the evening before for a mid-morning pickup.",
                 transport_back="Pre-booked Pathao/inDrive car, or shared jeep back via Bhaktapur.",
                 safe_until="10:00"),
        ],
        "stays": [
            dict(name="Nagarkot ridge guesthouses", stay_type="hotel", price_range="Rs 1,500–4,000/night",
                 verification_note="Multiple small hotels along the main ridge road with view rooms; several have "
                                    "female staff and are well used to solo women booking the sunrise package."),
        ],
    },
    {
        # Added from onboarding-survey demand: "Rooftop with mountain view" was the
        # 3rd most-picked activity (4/14 respondents) with no matching experience yet.
        "name": "Thamel rooftop sunset viewpoint",
        "area": "Thamel, Kathmandu",
        "description": (
            "A cluster of rooftop bars and restaurants above Thamel Chowk — Roof Café, Fat Monk's, "
            "Temple Town — where the Himalaya shows up over the rooftops on a clear day, especially "
            "post-monsoon (Oct–Nov). Sit for the view at golden hour, stay for live music some weekends."
        ),
        "latitude": "27.715600", "longitude": "85.310800",
        "vibe_tags": ["romantic", "social", "cozy"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="16:30", time_end="18:30",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Golden-hour mountain view on clear days, dinner-crowd staffing, easy solo table"),
            dict(day_type="weekend", time_start="19:00", time_end="22:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Bar atmosphere, occasional live music (Roof Café), stick to seated table service"),
        ],
        "safety": [
            dict(category="transport",
                 content="Walkable from any Thamel hotel (5–10 min). Pathao/inDrive for hotels further out, 10–15 min."),
            dict(category="area_safety",
                 content="Reputable rooftop venues have door staff and table service; treat it like any bar scene — "
                         "keep your own drink in sight, and it's a normal, comfortable solo hangout before ~10pm.",
                 safe_until="22:00"),
            dict(category="connectivity", content="Full 4G/5G, wifi at most rooftop venues."),
            dict(category="local_attitude",
                 content="Mixed tourist/local bar crowd, generally respectful; staff at established venues are quick "
                         "to intervene if a stranger won't take a polite no."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Tourist Police booth at Thamel Chowk, a few minutes' walk from any of these rooftops."),
            dict(category="return_route",
                 content="Ask the venue to call you a cab from the door rather than walking to a corner to hail one — "
                         "most rooftop bars do this routinely for solo guests.",
                 transport_back="Pathao/inDrive car, or walk directly back if your hotel is inside Thamel itself.",
                 safe_until="22:30"),
        ],
        "stays": [
            dict(name="Roof Café", stay_type="restaurant", price_range="Rs 500–1,200/item",
                 verification_note="Rooftop restaurant/bar with weekend live music and a mountain-view bonus; staffed table service."),
            dict(name="Fat Monk's Rooftop Bar", stay_type="restaurant", price_range="Rs 500–1,300/item",
                 verification_note="Cocktail-focused rooftop overlooking Thamel Chowk, popular sunset spot."),
        ],
    },
    {
        # Added from onboarding-survey demand: "Live music or concert" was the 2nd most-picked
        # activity (5/14 respondents) — nothing in the dataset carried an "energetic" vibe tag before this.
        "name": "Jazz Upstairs live music night",
        "area": "Lazimpat, Kathmandu",
        "description": (
            "A two-floor rooftop jazz bar in Lazimpat — Kathmandu's diplomatic quarter, and one of the "
            "better-lit, more heavily patrolled neighbourhoods in the city. Live jazz Wednesdays 8–10pm "
            "(sometimes Saturdays too), local beer, famous momos, dim vintage-cozy decor."
        ),
        "latitude": "27.720000", "longitude": "85.321400",
        "vibe_tags": ["energetic", "social", "romantic"],
        "solo_difficulty": 3,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="weekday", time_start="20:00", time_end="22:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Live jazz Wed 8–10pm (sometimes Sat), mixed local/expat regulars, dim lighting, dance-along vibe"),
        ],
        "safety": [
            dict(category="transport",
                 content="10–15 min / Rs 200–350 by Pathao/inDrive from Thamel; Lazimpat is close enough to walk from "
                         "northern Thamel in daylight, but take a ride at night."),
            dict(category="area_safety",
                 content="Lazimpat's embassy-district policing makes it one of the calmer, better-lit night areas in "
                         "the valley; the venue itself is small, staffed, and has a regular-crowd feel rather than a nightclub one.",
                 safe_until="22:30"),
            dict(category="connectivity", content="Good 4G throughout Lazimpat."),
            dict(category="local_attitude",
                 content="Live-jazz crowd skews musicians, expats, and regulars — noticeably more low-key and respectful "
                         "than generic nightclub scenes elsewhere in the city."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride to the venue's front door before the set ends (~10pm) — Lazimpat's main "
                         "road is well lit for a short wait.",
                 transport_back="Pathao/inDrive car back to Thamel or central Kathmandu, ~10–15 min.",
                 safe_until="22:30"),
        ],
        "stays": [
            dict(name="Jazz Upstairs", stay_type="restaurant", price_range="Rs 400–900/item",
                 verification_note="The venue itself — 2-floor rooftop jazz bar, food + drinks, friendly regular staff.",
                 contact="+977 1-4516983"),
        ],
    },
    {
        # Added from onboarding-survey demand: "Cafe hop somewhere pretty" (2/14) plus general
        # validation that a walkable, low-hassle daytime social spot was under-represented.
        "name": "Jhamsikhel café-hop trail",
        "area": "Jhamsikhel, Lalitpur",
        "description": (
            "Jhamel — a roughly 600m stretch of Jhamsikhel Road plus neighbouring Sanepa — is the "
            "valley's best café crawl: garden coffee spots, bookish cafés, boutiques, and cocktail bars "
            "packed within a few minutes' walk of each other. The most relaxed, foot-traffic-heavy "
            "neighbourhood in the valley for a solo afternoon."
        ),
        "latitude": "27.671700", "longitude": "85.312900",
        "vibe_tags": ["cozy", "social"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="10:00", time_end="18:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Garden cafés full of laptop workers, students, young professionals — easy to sit alone anywhere"),
            dict(day_type="weekend", time_start="18:00", time_end="21:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Strip lights up, cocktail bars open, still a walkable, well-populated crowd"),
        ],
        "safety": [
            dict(category="transport",
                 content="15–20 min / Rs 300–500 by Pathao/inDrive from Thamel or Patan Durbar Square. "
                         "Once there, everything worth visiting is within a 10-minute walk."),
            dict(category="area_safety",
                 content="Affluent, residential, constant foot traffic from locals doing exactly what you're doing — "
                         "widely considered the most relaxed neighbourhood in the valley for a woman alone, day into evening.",
                 safe_until="21:00"),
            dict(category="connectivity", content="Full 4G/5G, wifi at essentially every café on the strip."),
            dict(category="local_attitude",
                 content="Young-professional, expat-friendly crowd; solo women working from cafés here draw zero "
                         "attention — this is the low-hassle benchmark other spots get compared to."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="The strip stays lit and active until ~9–10pm; order a ride from any café doorway rather "
                         "than a side street.",
                 transport_back="Pathao/inDrive car back to Thamel or Patan, ~15–20 min.",
                 safe_until="21:00"),
        ],
        "stays": [
            dict(name="Cafe Soma", stay_type="cafe", price_range="Rs 300–700/item",
                 verification_note="Bohemian, book-filled café — a favourite solo work-and-read spot in Jhamel."),
            dict(name="Jalpa Coffee Club", stay_type="cafe", price_range="Rs 300–800/item",
                 verification_note="Leafy garden seating, opens 7am, known for breakfast — good early-morning solo stop."),
            dict(name="Himalayan Java, Jhamsikhel", stay_type="cafe", price_range="Rs 250–600/item",
                 verification_note="Reliable local chain, clean and consistent, easiest fallback if other spots are full."),
        ],
    },
    {
        # Added after feedback that the dataset leaned too heavily on mainstream, high-footfall
        # landmarks. This batch is deliberately off the standard tourist circuit, cross-checked
        # for road quality since bad access was the other explicit complaint.
        "name": "Bajrayogini Temple, Sankhu",
        "area": "Sankhu, Kathmandu",
        "description": (
            "Sankhu is a working Newari town on the valley's northeastern edge that most visitors "
            "never reach — no tour buses, no souvenir stalls. A forest path climbs about 2km from the "
            "town to the Bajrayogini Temple, an ancient hilltop shrine with valley and forest views. "
            "This is a real hidden gem, not a repackaged mainstream stop."
        ),
        "latitude": "27.741900", "longitude": "85.454500",
        "vibe_tags": ["peaceful", "contemplative"],
        "solo_difficulty": 3,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="08:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="A trickle of local pilgrims, forest birdsong, genuinely uncrowded rather than just quiet-for-Kathmandu"),
        ],
        "safety": [
            dict(category="transport",
                 content="45–60 min / Rs 900–1,300 by Pathao/inDrive — smooth paved road the whole way "
                         "(Araniko Highway, then a well-maintained local road into Sankhu), no rough or unpaved "
                         "stretches. Local buses from Ratna Park or Koteshwor also run direct to Sankhu (Rs 40–60, slower)."),
            dict(category="area_safety",
                 content="Sankhu's old town is safe and lived-in all day. The 2km forest path up to the temple is "
                         "genuinely quiet — comfortable with the steady trickle of local walkers, but this is one "
                         "where going with a buddy beats going solo for a first visit.",
                 safe_until="17:00"),
            dict(category="connectivity", content="Decent 4G in Sankhu town itself; patchy to none on the forest path up to the temple."),
            dict(category="local_attitude",
                 content="A real town, not a tourist stop — locals are welcoming but not especially used to visitors, "
                         "so expect curiosity rather than a polished welcome. Low hassle either way."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from Sankhu's town center, not the forest trailhead — better signal, "
                         "easier for a driver to find you.",
                 transport_back="Pathao/inDrive car back to Kathmandu, 45–60 min on the same paved road.",
                 safe_until="17:00"),
        ],
        "stays": [],
    },
    {
        "name": "Godawari Botanical Garden",
        "area": "Godawari, Lalitpur",
        "description": (
            "Nepal's oldest and largest botanical garden, at the valley's southern edge below Phulchowki. "
            "Genuinely quiet paths, a rose garden, greenhouses, and a forest trail at the back — except "
            "Friday and Saturday, when school trips and local families fill it up. Go on a weekday."
        ),
        "latitude": "27.596700", "longitude": "85.383300",
        "vibe_tags": ["peaceful"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_500",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="weekday", time_start="09:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Quiet paths, greenhouse, rose garden — genuinely calm on any day except Friday"),
            dict(day_type="weekend", time_start="09:00", time_end="16:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="School trips and family picnics — same garden, very different atmosphere"),
        ],
        "safety": [
            dict(category="transport",
                 content="35–45 min / Rs 700–1,000 by Pathao/inDrive via the Satdobato–Godavari Road — fully paved, "
                         "well-maintained the entire way, one of the easier drives on this list."),
            dict(category="area_safety",
                 content="A gated, ticketed, staffed public garden — safe and calm to sit alone in on a weekday.",
                 safe_until="16:00"),
            dict(category="connectivity", content="Good 4G throughout the garden."),
            dict(category="local_attitude", content="Garden staff and the handful of weekday visitors are low-key; "
                                                      "avoid Friday and Saturday if you specifically want it empty."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the main gate; garden closes in the late afternoon so don't linger past posted hours.",
                 transport_back="Pathao/inDrive car back to Patan or Kathmandu, ~35–45 min on the same paved road.",
                 safe_until="16:00"),
        ],
        "stays": [],
    },
    {
        "name": "Bishankhu Narayan cave temple",
        "area": "Godawari, Lalitpur",
        "description": (
            "A Vishnu shrine set inside a natural cave on a forested hillside about an hour's walk past "
            "the botanical garden — one of the valley's more obscure pilgrimage spots, with almost no "
            "foreign-tourist visibility at all."
        ),
        "latitude": "27.588000", "longitude": "85.395000",
        "vibe_tags": ["peaceful", "contemplative"],
        "solo_difficulty": 3,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="15:00",
                 crowd_level="low", solo_comfortable=False,
                 vibe_notes="Forest path with very few other walkers — pair up via the app's buddy feature rather than going alone"),
        ],
        "safety": [
            dict(category="transport",
                 content="Drive to Godawari Botanical Garden first (35–45 min / Rs 700–1,000 by Pathao/inDrive, "
                         "paved road throughout), then it's roughly an hour's walk on a forest trail from there — "
                         "there's no vehicle road all the way to the shrine itself."),
            dict(category="area_safety",
                 content="Quiet forest trail with genuinely low foot traffic — this is one of the least-visited "
                         "spots in the valley, which cuts both ways: peaceful, but not a solo-first-visit pick.",
                 safe_until="15:00"),
            dict(category="connectivity", content="No reliable signal on the forest trail — tell someone your route and expected return time first."),
            dict(category="local_attitude", content="Very few visitors of any kind; the odd local pilgrim is welcoming."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Nearest help is back at Godawari village."),
            dict(category="return_route",
                 content="Retrace the same trail back to Godawari Botanical Garden's gate before requesting a ride — "
                         "signal only returns there.",
                 transport_back="Pathao/inDrive car from Godawari back to Patan/Kathmandu, ~35–45 min.",
                 safe_until="15:00"),
        ],
        "stays": [],
    },
    {
        "name": "Vajra Varahi sacred forest",
        "area": "Chapagaon, Lalitpur",
        "description": (
            "A shaded forest grove around a 17th-century temple to Vajra Varahi, south of Patan past the "
            "village of Chapagaon. A genuine local spot rather than a tour-circuit stop — quiet on "
            "weekdays, but wedding parties and picnicking families do descend on it on Saturdays."
        ),
        "latitude": "27.610000", "longitude": "85.315000",
        "vibe_tags": ["peaceful", "contemplative"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="weekday", time_start="08:00", time_end="17:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Shaded grove, birdsong, a handful of pilgrims — genuinely calm"),
            dict(day_type="weekend", time_start="08:00", time_end="17:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Wedding parties and picnicking families fill the grove on Saturdays — still safe, just not quiet"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from Patan — paved road to Chapagaon village "
                         "the whole way, no rough sections."),
            dict(category="area_safety",
                 content="A quiet village-adjacent forest grove with local foot traffic through the day.",
                 safe_until="17:00"),
            dict(category="connectivity", content="Decent 4G in Chapagaon village, patchier inside the grove itself."),
            dict(category="local_attitude", content="A genuine community and pilgrimage site — welcoming, low hassle, "
                                                      "not set up for foreign tourism the way the valley's big three squares are."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from Chapagaon village center rather than the grove itself.",
                 transport_back="Pathao/inDrive car back to Patan, ~30–40 min on the same paved road.",
                 safe_until="17:00"),
        ],
        "stays": [],
    },
    {
        "name": "Jamacho Gumba forest hike",
        "area": "Nagarjun, Kathmandu",
        "description": (
            "The Nagarjun side of Shivapuri Nagarjun National Park — a separate forested hill from the "
            "valley's more-hiked Shivapuri peak, topped by the Jamacho Gumba monastery and a Himalayan "
            "viewpoint. Close to the city (near Balaju) but genuinely under-visited compared to Shivapuri "
            "or Swayambhunath."
        ),
        "latitude": "27.746000", "longitude": "85.265000",
        "vibe_tags": ["peaceful", "adventurous"],
        "solo_difficulty": 4,
        "min_comfort_tier": "confident",
        "budget_tier": "under_500",
        "scene_type": "hidden_gem",
        "best_months": [6, 7, 8, 12, 1],
        "windows": [
            dict(day_type="any", time_start="07:00", time_end="14:00",
                 crowd_level="low", solo_comfortable=False,
                 vibe_notes="Forested park trail, very few other hikers — go with a buddy, not solo"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–600 by Pathao/inDrive from Thamel to Fulbari Gate near Balaju/Machha "
                         "Pokhari — paved city road the entire way, one of the closer and easier-access hikes in the valley."),
            dict(category="area_safety",
                 content="Ticketed national park entrance with a ranger post, but the forest trail up to the gumba "
                         "sees few visitors — pair up via the app's buddy feature rather than hiking alone.",
                 safe_until="15:00"),
            dict(category="connectivity", content="Little to no signal once inside the forest — share your route and expected return time before you start."),
            dict(category="local_attitude", content="Park rangers and the resident monks at Jamacho Gumba are helpful; "
                                                      "you're unlikely to meet many other people on the trail itself."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Sign the trail register at the Fulbari Gate ranger post on the way in."),
            dict(category="return_route",
                 content="Aim to be back at Fulbari Gate by 3pm — signal and ride-hailing only reliably work again once you're back at the gate.",
                 transport_back="Pathao/inDrive car from Fulbari Gate back to Kathmandu, ~20–30 min.",
                 safe_until="15:30"),
        ],
        "stays": [],
    },
    {
        # Second hidden-gem batch. Note: Lele Valley was researched and deliberately left out —
        # sources disagreed on its road (one rated it 8/10, another described "off-road terrain
        # for most of your trip"), which fails the explicit good-road-condition bar for this list.
        "name": "Lakuri Bhanjyang ridge viewpoint",
        "area": "Lakuri Bhanjyang, Lalitpur",
        "description": (
            "A ridge hill station on the valley's southeastern edge — panoramic Himalaya and valley "
            "views, popular with local cyclists, genuinely uncrowded compared to Nagarkot or Chandragiri. "
            "Fully paved road the entire way, one of the smoothest drives on this list."
        ),
        "latitude": "27.617000", "longitude": "85.370000",
        "vibe_tags": ["peaceful", "adventurous"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="weekday", time_start="07:00", time_end="17:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Open ridge, scattered cyclists and teashop owners, genuinely uncrowded"),
            dict(day_type="weekend", time_start="09:00", time_end="16:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Day-trippers and mountain bikers out, still far calmer than Nagarkot or Chandragiri"),
        ],
        "safety": [
            dict(category="transport",
                 content="40–45 min / Rs 800–1,100 by Pathao/inDrive from Patan — fully paved road the entire "
                         "~15km from Gwarko Chowk, one of the smoothest drives on this list. Public buses from "
                         "Gwarko also run partway."),
            dict(category="area_safety",
                 content="A genuine local cycling and day-trip spot rather than a tour-bus destination — open "
                         "ridge with scattered visitors through the day.",
                 safe_until="17:00"),
            dict(category="connectivity", content="Decent 4G at the viewpoint itself, patchier on the approach road."),
            dict(category="local_attitude", content="Cyclists, local day-trippers, and a handful of teashop owners — relaxed, low-hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works fine from the main viewpoint area; head back before dark since the "
                         "ridge road has no streetlighting.",
                 transport_back="Pathao/inDrive car back to Patan/Gwarko, ~40–45 min on the same paved road.",
                 safe_until="17:30"),
        ],
        "stays": [
            dict(name="Lakuri Bhanjyang viewpoint teashops", stay_type="cafe", price_range="Rs 100–300/item",
                 verification_note="Simple family-run teashops along the ridge, open daytime for tea and noodles."),
        ],
    },
    {
        "name": "Sundarijal waterfall and dam",
        "area": "Sundarijal, Kathmandu",
        "description": (
            "A green, waterfall-and-dam village at the valley's northeastern edge, marking the start of "
            "Kathmandu's water supply system and the trailhead for hikes toward Chisapani and Nagarkot. "
            "Quiet in its own right even though trekking groups pass through."
        ),
        "latitude": "27.783300", "longitude": "85.433300",
        "vibe_tags": ["peaceful", "adventurous"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_500",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="07:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Waterfall and dam-side walk, quiet outside of trekking groups passing through"),
        ],
        "safety": [
            dict(category="transport",
                 content="35–45 min / Rs 700–1,000 by Pathao/inDrive, or a direct public bus from Ratna Park "
                         "(Rs 30–40) — paved road the whole way, since Sundarijal is Kathmandu's water-supply "
                         "area and the access road is maintained infrastructure, not a rough track."),
            dict(category="area_safety",
                 content="The village and waterfall/dam area see a steady trickle of locals and trekkers heading "
                         "further into the park; calm and low-hassle right at the dam itself.",
                 safe_until="16:30"),
            dict(category="connectivity", content="Good 4G in the village, patchy once you're on the forest trail beyond it."),
            dict(category="local_attitude", content="Mixed locals and trekkers passing through toward Chisapani/Nagarkot — welcoming, low hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Police post in Sundarijal village."),
            dict(category="return_route",
                 content="Order your ride from the village/bus stop rather than the trail; public buses run until early evening.",
                 transport_back="Public bus or Pathao/inDrive back to Kathmandu, ~35–45 min.",
                 safe_until="17:00"),
        ],
        "stays": [
            dict(name="Sundarijal teahouses", stay_type="restaurant", price_range="Rs 150–400/item",
                 verification_note="Simple teahouses near the dam, popular rest stop for trekkers heading up toward Chisapani."),
        ],
    },
    {
        "name": "Dakshinkali Temple",
        "area": "Pharping, Kathmandu",
        "description": (
            "A major Kali temple at the confluence of two rivers, set in forest at the valley's southern "
            "edge — a genuine working pilgrimage site, not an international tourist stop. Calm most of the "
            "week; Tuesdays and Saturdays are puja days and draw heavy crowds, including animal sacrifice "
            "rituals that can be intense to witness."
        ),
        "latitude": "27.590000", "longitude": "85.283300",
        "vibe_tags": ["contemplative", "peaceful"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="weekday", time_start="09:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Calm forest-temple atmosphere most weekdays — except Tuesday specifically, a puja day that draws heavy crowds"),
            dict(day_type="weekend", time_start="09:00", time_end="16:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Saturday is the temple's busiest puja day — packed with worshippers; go a different day if you want it quiet"),
        ],
        "safety": [
            dict(category="transport",
                 content="35–45 min / Rs 700–1,000 by Pathao/inDrive via Dakshinkali Road — fully paved and "
                         "well-maintained given the volume of pilgrim traffic it handles. Public buses run direct from Kathmandu too."),
            dict(category="area_safety",
                 content="A heavily-visited, functioning pilgrimage site with a constant flow of worshippers and "
                         "temple staff — safe and normal to visit alone any day. Be aware it includes animal "
                         "sacrifice rituals, which some visitors find distressing to witness.",
                 safe_until="16:00"),
            dict(category="connectivity", content="Decent 4G throughout."),
            dict(category="local_attitude", content="Welcoming to visitors of all backgrounds; a genuine working "
                                                      "temple rather than a tourist attraction, so dress and behave respectfully."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works reliably from the temple's main parking area.",
                 transport_back="Pathao/inDrive car back to Kathmandu, ~35–45 min on the same paved road.",
                 safe_until="16:30"),
        ],
        "stays": [],
    },
    {
        # Third hidden-gem batch, deliberately targeting "energy" and "wonder" moods —
        # those two were thin (one real energetic place, almost nothing tagged "cozy"),
        # and more temples wasn't going to fix that. These are real commercial recreation
        # venues used by locals, not tourist attractions, all in developed city areas
        # with normal paved city-street access.
        "name": "Jump KTM Trampoline Park",
        "area": "Mandikatar, Kathmandu",
        "description": (
            "Nepal's first indoor trampoline park — free-jump area, dodgeball court, slam-dunk lanes, "
            "airbags. A genuine local hangout for teenagers and young adults, not a tourist attraction "
            "at all, and a rare 'energy' option that isn't nightlife or a bar."
        ),
        "latitude": "27.725000", "longitude": "85.355000",
        "vibe_tags": ["energetic", "social"],
        "solo_difficulty": 2,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="weekday", time_start="11:00", time_end="18:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Mixed groups, some solo teens practicing tricks — easy to join in without a group"),
            dict(day_type="weekend", time_start="10:00", time_end="19:00",
                 crowd_level="high", solo_comfortable=True,
                 vibe_notes="Packed with families and groups — energetic, loud, fun rather than crowded-uncomfortable"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–600 by Pathao/inDrive from Thamel — normal paved city streets "
                         "the whole way, no access concerns at all."),
            dict(category="area_safety",
                 content="A staffed, ticketed indoor venue with attendants supervising the equipment at all times — "
                         "as controlled and safe a solo outing as exists on this list.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Full 4G indoors."),
            dict(category="local_attitude", content="Young, mixed-gender local crowd; completely normal to show up alone and join in."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works fine right from the entrance.",
                 transport_back="Pathao/inDrive car back to central Kathmandu, ~20–30 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Play Zone Nakhipot",
        "area": "Nakhipot, Lalitpur",
        "description": (
            "An indoor activity center — trampolines, a climbing wall, bull ride, wipeout course — in "
            "a developed part of Lalitpur. A genuine multi-activity 'energy' venue that also scratches "
            "the adventurous itch of 'wonder' mood, without needing a forest hike to get there."
        ),
        "latitude": "27.650000", "longitude": "85.320000",
        "vibe_tags": ["energetic", "social", "adventurous"],
        "solo_difficulty": 2,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="11:00", time_end="19:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Local families and groups, staffed attractions, easy to drop in solo"),
        ],
        "safety": [
            dict(category="transport",
                 content="25–35 min / Rs 500–700 by Pathao/inDrive from Patan — paved road throughout, "
                         "Nakhipot is a developed residential/commercial area on the Ring Road."),
            dict(category="area_safety",
                 content="Staffed, ticketed indoor venue with attendants on every attraction.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Full 4G indoors."),
            dict(category="local_attitude", content="Local family crowd, low hassle, normal to visit alone."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works fine right from the entrance.",
                 transport_back="Pathao/inDrive car back to Patan, ~25–35 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Astrek Climbing Wall",
        "area": "Thamel, Kathmandu",
        "description": (
            "Nepal's tallest indoor climbing wall (50 feet, routes from beginner to expert) tucked inside "
            "the Astrek Complex in Thamel — a real adventure-sport gym used by climbers and expats, not "
            "a stop on anyone's sightseeing itinerary despite being in the middle of the tourist district."
        ),
        "latitude": "27.715000", "longitude": "85.311000",
        "vibe_tags": ["adventurous", "energetic"],
        "solo_difficulty": 2,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="10:00", time_end="18:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="A small, dedicated climbing crowd — instructors on hand, easy to show up solo and rent gear"),
        ],
        "safety": [
            dict(category="transport",
                 content="Walkable from any Thamel hotel (5–10 min); Pathao/inDrive from elsewhere in the city, "
                         "10–20 min on normal paved streets."),
            dict(category="area_safety",
                 content="A small, staffed gym with instructors present for belaying and safety checks at all times.",
                 safe_until="18:00"),
            dict(category="connectivity", content="Full 4G/5G, Thamel wifi coverage."),
            dict(category="local_attitude", content="Climbing-community crowd — welcoming, used to solo climbers of all levels showing up alone."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Tourist Police booth a few minutes away at Thamel Chowk."),
            dict(category="return_route",
                 content="Walk back if staying in Thamel; otherwise order a ride from the complex entrance.",
                 transport_back="Pathao/inDrive car, 10–20 min depending on destination.",
                 safe_until="18:30"),
        ],
        "stays": [],
    },
    {
        "name": "Funland Bhadrakali",
        "area": "Bhadrakali, Kathmandu",
        "description": (
            "An indoor amusement center near Ratna Park — ice skating, bull ride, rock climbing, "
            "trampoline, ninja-style obstacle training. A genuine local family entertainment spot in "
            "the heart of the city, easy to reach, not aimed at tourists at all."
        ),
        "latitude": "27.705000", "longitude": "85.315000",
        "vibe_tags": ["energetic", "social"],
        "solo_difficulty": 2,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="11:00", time_end="19:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Families and groups of friends, staffed attractions throughout"),
        ],
        "safety": [
            dict(category="transport",
                 content="10–15 min / Rs 250–400 by Pathao/inDrive from Thamel — central Kathmandu, normal paved streets."),
            dict(category="area_safety",
                 content="Staffed, ticketed indoor venue in a busy, well-lit central part of the city.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Full 4G indoors and in the surrounding area."),
            dict(category="local_attitude", content="Local family and youth crowd, low hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Central location — ride-hailing and taxis are easy to find right outside.",
                 transport_back="Pathao/inDrive car back to Thamel or anywhere central, 10–15 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Thimi Pottery Square",
        "area": "Madhyapur Thimi, Bhaktapur",
        "description": (
            "A working potters' square in Thimi — less touristy than nearby Bhaktapur, where you can "
            "watch (or try) traditional wheel-thrown pottery with local artisans. A genuinely hands-on, "
            "unhurried craft experience rather than a sightseeing stop."
        ),
        "latitude": "27.683300", "longitude": "85.383300",
        "vibe_tags": ["cozy", "contemplative"],
        "solo_difficulty": 2,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="08:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Potters at their wheels, side streets quiet, genuinely local rather than staged for visitors"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from Kathmandu — paved road via the Araniko "
                         "Highway/Bhaktapur road the whole way."),
            dict(category="area_safety",
                 content="A lived-in artisan neighbourhood with constant local foot traffic — safe and calm to walk alone.",
                 safe_until="16:30"),
            dict(category="connectivity", content="Decent 4G throughout."),
            dict(category="local_attitude", content="Working artisans, used to a handful of visitors — welcoming, low hassle, genuine interaction if you ask about their craft."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the main square rather than a side lane.",
                 transport_back="Pathao/inDrive car back to Kathmandu or Bhaktapur, ~30–40 min.",
                 safe_until="17:00"),
        ],
        "stays": [],
    },
    {
        "name": "Taragaon Next museum",
        "area": "Boudha, Kathmandu",
        "description": (
            "A small private gallery of 18th–19th century photographs, watercolors, and maps documenting "
            "the Kathmandu Valley, set on the grounds of a hotel near Boudhanath. Genuinely obscure — "
            "most people in the city don't know it exists, let alone visitors."
        ),
        "latitude": "27.720800", "longitude": "85.360500",
        "vibe_tags": ["cozy", "contemplative"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_500",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="10:00", time_end="17:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Almost always quiet — a handful of visitors at most, staffed and comfortable to browse alone"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–700 by Pathao/inDrive from Thamel — same paved road into Boudha as the stupa."),
            dict(category="area_safety",
                 content="A small, staffed gallery on hotel grounds — calm and safe to visit alone any time it's open.",
                 safe_until="17:00"),
            dict(category="connectivity", content="Good 4G, wifi on-site."),
            dict(category="local_attitude", content="Gallery staff are attentive and low-key; very few other visitors to navigate around."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the hotel grounds entrance.",
                 transport_back="Pathao/inDrive car back to Thamel or central Kathmandu, ~20–30 min.",
                 safe_until="17:30"),
        ],
        "stays": [],
    },
    {
        "name": "Gokarna Forest",
        "area": "Gokarna, Kathmandu",
        "description": (
            "A 470-acre former royal hunting forest on the valley's edge, with centuries-old trees, "
            "spotted deer, and a Bagmati riverside walk — a genuine half-day nature escape a fraction "
            "of the distance of the valley-rim hikes."
        ),
        "latitude": "27.738300", "longitude": "85.396100",
        "vibe_tags": ["peaceful", "romantic"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_500",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="weekday", time_start="07:00", time_end="17:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Old-growth forest, deer, riverside quiet — genuinely uncrowded on weekdays"),
            dict(day_type="weekend", time_start="09:00", time_end="17:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Local families out walking, still far calmer than any of the valley's main parks"),
        ],
        "safety": [
            dict(category="transport",
                 content="25–35 min / Rs 500–800 by Pathao/inDrive from Thamel via Boudha — paved road the whole way "
                         "(the same route toward Sundarijal)."),
            dict(category="area_safety",
                 content="A managed, gated forest reserve with staff and a steady trickle of local walkers on weekdays.",
                 safe_until="17:00"),
            dict(category="connectivity", content="Decent 4G near the entrance, patchier deeper into the forest."),
            dict(category="local_attitude", content="Local walkers and joggers; low hassle, generally a peaceful, respectful crowd."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the main gate before the forest closes in the evening.",
                 transport_back="Pathao/inDrive car back to Kathmandu, ~25–35 min.",
                 safe_until="17:30"),
        ],
        "stays": [],
    },
    {
        "name": "Druk Amitabha Monastery",
        "area": "Nagarjun, Kathmandu",
        "description": (
            "A hilltop Buddhist nunnery (the 'Seto Gumba,' or White Monastery) about 3km north of "
            "Swayambhunath, surrounded by forest. Genuinely tranquil rather than merely quiet-for-Kathmandu — "
            "visitors come specifically for meditation and calm, not sightseeing."
        ),
        "latitude": "27.726900", "longitude": "85.279400",
        "vibe_tags": ["peaceful", "contemplative"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="08:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Resident nuns, forest quiet, a small trickle of meditation visitors"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–600 by Pathao/inDrive from Thamel via Swayambhu, then a short uphill "
                         "stretch — paved road most of the way with a final short climb. Microbuses toward "
                         "Nagarjun also run from central Kathmandu."),
            dict(category="area_safety",
                 content="A calm monastery compound with resident nuns and staff around through the day.",
                 safe_until="16:00"),
            dict(category="connectivity", content="Decent 4G on the approach road, patchier right at the monastery."),
            dict(category="local_attitude", content="Welcoming to respectful visitors — dress modestly, keep your voice down near the prayer halls."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the monastery's entrance gate rather than partway down the hill.",
                 transport_back="Pathao/inDrive car back to Kathmandu, ~20–30 min.",
                 safe_until="16:30"),
        ],
        "stays": [],
    },
    {
        "name": "Khokana mustard-oil village",
        "area": "Khokana, Lalitpur",
        "description": (
            "A small, still-working Newari village on the outskirts of Patan, known for centuries-old "
            "traditional mustard-oil pressing. Quiet, lived-in brick lanes with almost no tourist presence — "
            "Bungamati's quieter twin village."
        ),
        "latitude": "27.648600", "longitude": "85.298900",
        "vibe_tags": ["peaceful", "contemplative"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="16:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Oil-pressing courtyards, quiet brick lanes, genuine village life rather than a sightseeing stop"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from Patan — paved road via Ring Road south "
                         "toward Bungamati/Khokana, the same route as the Karya Binayak viewpoint."),
            dict(category="area_safety",
                 content="A small, lived-in village with constant local foot traffic through the day.",
                 safe_until="16:30"),
            dict(category="connectivity", content="Basic 4G, can drop to 3G in the older lanes."),
            dict(category="local_attitude", content="Very low tourist volume means more curiosity than hassle; residents are welcoming if approached respectfully."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the village center; signal can be weak in the inner lanes.",
                 transport_back="Pathao/inDrive car back to Patan, ~30–40 min.",
                 safe_until="16:30"),
        ],
        "stays": [],
    },
    {
        "name": "Sikali Temple",
        "area": "Khokana, Lalitpur",
        "description": (
            "A large three-storey temple to the goddess Sikali (Rudrayani), set in an open green meadow "
            "just outside Khokana village, ringed by paddy fields and hills. Genuinely obscure outside "
            "one week a year: locals hold the five-day Sikali Jatra festival here around Ghatasthapana "
            "(the start of Dashain, roughly September/October), when it's the busiest place in the area — "
            "the rest of the year it's just an open, quiet field."
        ),
        "latitude": "27.647000", "longitude": "85.297500",
        "vibe_tags": ["contemplative", "peaceful", "romantic"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "scene_type": "hidden_gem",
        "windows": [
            dict(day_type="any", time_start="06:00", time_end="17:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Open meadow, paddy fields, hills in every direction — genuinely quiet most of the year"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from Patan — paved road to Khokana village "
                         "(same route as the mustard-oil village), then a 15-minute walk through fields to the "
                         "temple meadow. Local buses from Ekantakuna toward Khokana also run regularly."),
            dict(category="area_safety",
                 content="An open field on the village edge — calm during the day with occasional local foot "
                         "traffic; it empties out toward evening, so this is a daytime visit rather than a sunset-lingering one.",
                 safe_until="17:00"),
            dict(category="connectivity", content="Basic 4G, patchier out in the open field than in the village itself."),
            dict(category="local_attitude", content="Very low visitor volume outside festival week — respectful, low-hassle if you do meet locals working the fields."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Walk back into Khokana village center to order a ride — signal and driver pin accuracy are both better there than out in the field.",
                 transport_back="Pathao/inDrive car back to Patan, ~30–40 min.",
                 safe_until="17:00"),
        ],
        "stays": [],
    },
    {
        # Sunset-viewpoint batch, requested directly — both road-accessible, both
        # explicitly described in research as hidden-gem alternatives to Nagarkot/Chandragiri.
        "name": "Ranikot viewpoint",
        "area": "Suryabinayak, Bhaktapur",
        "description": (
            "A forested hilltop above the Suryabinayak Temple area near Bhaktapur, with a genuine "
            "180-degree view of the Himalaya and the valley — a real alternative to Nagarkot for sunset "
            "without the tour-bus crowd."
        ),
        "latitude": "27.665000", "longitude": "85.415000",
        "vibe_tags": ["romantic", "peaceful"],
        "solo_difficulty": 3,
        "min_comfort_tier": "cautious",
        "budget_tier": "free",
        "windows": [
            dict(day_type="any", time_start="15:30", time_end="18:00",
                 crowd_level="low", solo_comfortable=False,
                 vibe_notes="Forested hilltop, genuinely uncrowded even at golden hour — pair up rather than go alone for a first visit"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from Kathmandu to Suryabinayak Chowk near "
                         "Bhaktapur — paved road the whole way, then a signed local road up toward Suryabinayak "
                         "Temple and the Ranikot trail beyond it."),
            dict(category="area_safety",
                 content="A quiet forested viewpoint with very few visitors — genuinely peaceful, but the "
                         "low foot traffic is exactly why a buddy beats going solo here, especially near sunset "
                         "when light fades fast under trees.",
                 safe_until="18:00"),
            dict(category="connectivity", content="Patchy 4G on the hilltop itself, better near Suryabinayak Temple below."),
            dict(category="local_attitude", content="A handful of local hikers and temple visitors; low hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102. "
                         "Suryabinayak Temple below has a regular flow of people if you need help quickly."),
            dict(category="return_route",
                 content="Head back down to Suryabinayak Chowk before dark — no lighting on the hill road, "
                         "and ride-hailing works far more reliably down at the chowk.",
                 transport_back="Pathao/inDrive car from Suryabinayak Chowk back to Kathmandu/Bhaktapur, ~30–40 min.",
                 safe_until="18:00"),
        ],
        "stays": [],
    },
    {
        "name": "Kankali View Tower",
        "area": "Nagarjun, Kathmandu",
        "description": (
            "A viewpoint tower in the Nagarjun area with a sweeping look over Kathmandu's urban sprawl, "
            "green patches, and the surrounding hills — a genuine hidden-gem sunset spot with an actual "
            "resort on-site, meaning real road access rather than a bare hilltop."
        ),
        "latitude": "27.750000", "longitude": "85.270000",
        "vibe_tags": ["romantic", "peaceful"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_500",
        "windows": [
            dict(day_type="any", time_start="15:00", time_end="18:30",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Sweeping valley views, genuinely quiet compared to Chandragiri or Nagarkot at the same hour"),
        ],
        "safety": [
            dict(category="transport",
                 content="25–35 min / Rs 500–800 by Pathao/inDrive from Thamel toward Nagarjun — paved road, "
                         "the same general direction as Jamacho Gumba and Druk Amitabha Monastery."),
            dict(category="area_safety",
                 content="An actual resort/viewpoint property with staff on-site — one of the more comfortable "
                         "solo sunset spots on this list precisely because it isn't a bare, unstaffed hilltop.",
                 safe_until="18:30"),
            dict(category="connectivity", content="Decent 4G, better than most forest viewpoints since there's a working resort here."),
            dict(category="local_attitude", content="Resort staff and a small, low-key visitor crowd; welcoming to solo travelers."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the property entrance before full dark.",
                 transport_back="Pathao/inDrive car back to Kathmandu, ~25–35 min.",
                 safe_until="19:00"),
        ],
        "stays": [
            dict(name="Kankali Viewpoint Resort", stay_type="restaurant", price_range="Rs 500–1,200/meal",
                 verification_note="On-site restaurant/resort with valley views — staffed daily, a comfortable place to watch sunset from."),
        ],
    },
]

# Peaceful garden-café batch, requested directly: real, individually named quiet cafés
# spread across the valley — not the nightlife/rooftop "cafe_social" spots already seeded,
# but calm, garden-set places that actually serve the "peace" mood. Each is its own
# Experience (not folded into an area cluster) since each has a genuinely distinct location
# and character. "Garden of Dreams" was on the requested list but is already seeded
# (Thamel, Kathmandu, mainstream) — not duplicated here.
CAFE_PLACES = [
    {
        "name": "Tavera Inn",
        "area": "Swayambhu, Kathmandu",
        "description": (
            "An aesthetic garden café-resort near White Gumba, 10 minutes from Swayambhunath, with "
            "city views and vegetarian dishes built around a calm, unhurried daycation feel rather than "
            "a quick coffee stop."
        ),
        "latitude": "27.716700", "longitude": "85.291700",
        "vibe_tags": ["peaceful", "cozy", "romantic"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="10:00", time_end="18:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Garden seating, city views, genuinely unhurried — a daycation vibe, not a quick-coffee crowd"),
        ],
        "safety": [
            dict(category="transport",
                 content="15–20 min / Rs 300–500 by Pathao/inDrive from Thamel — paved road via Swayambhu, "
                         "same general route as the stupa."),
            dict(category="area_safety",
                 content="A staffed café-resort with parking and a gated setting — calm and easy to sit alone in all day.",
                 safe_until="18:00"),
            dict(category="connectivity", content="Good 4G, likely wifi on-site."),
            dict(category="local_attitude", content="Café staff and a low-key local crowd; comfortable for solo visitors."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the property entrance.",
                 transport_back="Pathao/inDrive car back to Thamel, ~15–20 min.",
                 safe_until="18:30"),
        ],
        "stays": [],
    },
    {
        "name": "Windy Hill Hotel and Restaurant",
        "area": "Bungamati, Lalitpur",
        "description": (
            "A cozy hillside mini-resort and restaurant near Karyabinayak/Bungamati, with breathtaking "
            "valley views from a gentle hilltop setting — genuinely peaceful rather than a tour stop, "
            "in the same quiet corner of the valley as the Karya Binayak viewpoint."
        ),
        "latitude": "27.641000", "longitude": "85.306500",
        "vibe_tags": ["peaceful", "cozy", "romantic"],
        "solo_difficulty": 2,
        "min_comfort_tier": "cautious",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="10:00", time_end="18:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Hilltop garden seating, valley views, genuinely quiet"),
        ],
        "safety": [
            dict(category="transport",
                 content="30–40 min / Rs 600–900 by Pathao/inDrive from Patan via the Ekantakuna–Tikabhairab "
                         "road — paved throughout, the same route as Bungamati/Karya Binayak."),
            dict(category="area_safety",
                 content="A staffed hillside resort with a gated setting — calm and comfortable to sit alone in.",
                 safe_until="18:00"),
            dict(category="connectivity", content="Decent 4G on the hilltop."),
            dict(category="local_attitude", content="Resort staff and a small local crowd; low hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your ride from the property entrance before dusk — the hill road has no lighting.",
                 transport_back="Pathao/inDrive car back to Patan, ~30–40 min.",
                 safe_until="18:00"),
        ],
        "stays": [],
    },
    {
        "name": "Garden Project Restaurant",
        "area": "Bhanimandal, Lalitpur",
        "description": (
            "A quiet garden restaurant in Bhanimandal — genuinely pretty grounds, an unhurried spot to "
            "sit alone with a book or a coffee away from Patan's busier café strips."
        ),
        "latitude": "27.666700", "longitude": "85.328300",
        "vibe_tags": ["peaceful", "cozy"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="10:00", time_end="19:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Garden seating, generally quiet, easy solo table"),
        ],
        "safety": [
            dict(category="transport",
                 content="15–20 min / Rs 300–500 by Pathao/inDrive from Patan or Thamel — normal paved city streets."),
            dict(category="area_safety",
                 content="A staffed garden restaurant with on-site parking; calm and comfortable to sit alone.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Good 4G."),
            dict(category="local_attitude", content="Low-key local crowd, comfortable for solo visitors."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Patan or Thamel, ~15–20 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Yala Garden Cafe and Restaurant",
        "area": "Patan, Lalitpur",
        "description": (
            "A secluded garden café just off Patan's main streets — genuinely removed from the moped "
            "traffic and noise, one of the highest-rated quiet cafés in the area."
        ),
        "latitude": "27.672000", "longitude": "85.323000",
        "vibe_tags": ["peaceful", "cozy", "romantic"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="19:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Secluded garden seating, genuinely quiet despite being minutes from Patan Durbar Square"),
        ],
        "safety": [
            dict(category="transport",
                 content="15–25 min / Rs 300–500 by Pathao/inDrive from Thamel — same route as Patan Durbar Square."),
            dict(category="area_safety",
                 content="A staffed café with a gated garden setting — calm and easy to sit alone in.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Good 4G."),
            dict(category="local_attitude", content="Relaxed café crowd, low hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Thamel, ~15–25 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Utpala Cafe",
        "area": "Boudha, Kathmandu",
        "description": (
            "A vegetarian café set back from Boudha's main roads — a relaxing, low-noise spot to sit "
            "alone away from the kora crowds, rather than another stupa-view rooftop."
        ),
        "latitude": "27.721000", "longitude": "85.361500",
        "vibe_tags": ["peaceful", "cozy"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_500",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="19:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Set back from the main roads, genuinely calm compared to the stupa plaza cafés"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–700 by Pathao/inDrive from Thamel — same paved road into Boudha as the stupa."),
            dict(category="area_safety",
                 content="A quiet, staffed café off the main roads — calm and comfortable solo.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Good 4G."),
            dict(category="local_attitude", content="Low-key, relaxed crowd; vegetarian-focused menu draws a calmer clientele than the kora-side restaurants."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the café entrance.",
                 transport_back="Pathao/inDrive car back to Thamel, ~20–30 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Lavie Garden",
        "area": "Boudha, Kathmandu",
        "description": (
            "A greenery-filled garden restaurant in Boudha, good for a slow breakfast or dinner away "
            "from the stupa's tourist-facing strip."
        ),
        "latitude": "27.722000", "longitude": "85.363000",
        "vibe_tags": ["peaceful", "cozy", "social"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="08:00", time_end="20:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Greenery-filled garden seating, relaxed pace, easy solo table"),
        ],
        "safety": [
            dict(category="transport",
                 content="20–30 min / Rs 400–700 by Pathao/inDrive from Thamel — same paved road into Boudha as the stupa."),
            dict(category="area_safety",
                 content="A staffed garden restaurant, calm and comfortable solo through the evening.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Good 4G."),
            dict(category="local_attitude", content="Mixed local and long-term-expat crowd; relaxed and low-hassle."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Thamel, ~20–30 min.",
                 safe_until="20:30"),
        ],
        "stays": [],
    },
    {
        "name": "Salon de Kathmandu",
        "area": "Lazimpat, Kathmandu",
        "description": (
            "A café on a quiet Lazimpat side street, opening onto a vast rose garden — genuinely one of "
            "the prettiest, calmest sit-alone spots in the diplomatic quarter."
        ),
        "latitude": "27.719000", "longitude": "85.320500",
        "vibe_tags": ["peaceful", "romantic", "cozy"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="19:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Rose garden seating on a quiet side street — genuinely calm"),
        ],
        "safety": [
            dict(category="transport",
                 content="10–15 min / Rs 200–350 by Pathao/inDrive from Thamel — Lazimpat's embassy-district "
                         "roads are well maintained and well lit."),
            dict(category="area_safety",
                 content="A quiet side-street café in one of the better-policed, better-lit parts of the city.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Good 4G throughout Lazimpat."),
            dict(category="local_attitude", content="Low-key, relaxed clientele; comfortable for solo visitors."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Thamel, ~10–15 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Kyampa",
        "area": "Sanepa, Lalitpur",
        "description": (
            "A cozy, greenery-surrounded café-restaurant in Sanepa, right next to Jhamsikhel's café strip "
            "but a notch quieter — good for coffee, lunch, or a slow afternoon alone."
        ),
        "latitude": "27.680000", "longitude": "85.308000",
        "vibe_tags": ["cozy", "peaceful", "social"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="20:00",
                 crowd_level="medium", solo_comfortable=True,
                 vibe_notes="Cozy, greenery-filled seating, a notch quieter than the main Jhamsikhel strip nearby"),
        ],
        "safety": [
            dict(category="transport",
                 content="15–20 min / Rs 300–500 by Pathao/inDrive from Thamel or Patan — same general area as "
                         "the Jhamsikhel café-hop strip."),
            dict(category="area_safety",
                 content="Affluent, walkable residential-commercial neighbourhood — one of the most relaxed areas in the valley.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Full 4G/5G, wifi on-site."),
            dict(category="local_attitude", content="Young-professional, low-hassle crowd."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Thamel or Patan, ~15–20 min.",
                 safe_until="20:30"),
        ],
        "stays": [],
    },
    {
        "name": "Peaceful Restaurant",
        "area": "Bhaktapur",
        "description": (
            "A restaurant near Dattatreya Square with a genuinely quiet backyard garden — a calm sit-down "
            "option away from the main Durbar Square crowds, true to its name."
        ),
        "latitude": "27.672000", "longitude": "85.430000",
        "vibe_tags": ["peaceful", "cozy"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_500",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="19:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="A quiet backyard garden, genuinely calm even when the main square is busy"),
        ],
        "safety": [
            dict(category="transport",
                 content="35–45 min / Rs 700–1,000 by Pathao/inDrive from Thamel or Kathmandu Durbar Square — "
                         "same paved road as the rest of Bhaktapur."),
            dict(category="area_safety",
                 content="A staffed restaurant in the pedestrianized old town, calm and comfortable solo.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Good 4G throughout the old town."),
            dict(category="local_attitude", content="Low-key, relaxed local clientele away from the main square's tourist flow."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Order your car from one of the main squares nearby rather than a back lane.",
                 transport_back="Pathao/inDrive car back to Kathmandu, ~35–45 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "Pauline's Garden",
        "area": "Baluwatar, Kathmandu",
        "description": (
            "A tucked-away outdoor café on a tiny Baluwatar side street — a genuinely private-feeling "
            "garden space that feels like a small getaway despite being minutes from the city center."
        ),
        "latitude": "27.728000", "longitude": "85.332000",
        "vibe_tags": ["peaceful", "cozy", "romantic"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="19:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Tucked-away garden, private feel, genuinely quiet side street"),
        ],
        "safety": [
            dict(category="transport",
                 content="10–15 min / Rs 250–400 by Pathao/inDrive from Thamel — Baluwatar's diplomatic-adjacent "
                         "streets are well maintained."),
            dict(category="area_safety",
                 content="A quiet residential side street with a staffed café — calm and comfortable solo.",
                 safe_until="19:00"),
            dict(category="connectivity", content="Good 4G."),
            dict(category="local_attitude", content="Low-key, relaxed crowd."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Thamel, ~10–15 min.",
                 safe_until="19:30"),
        ],
        "stays": [],
    },
    {
        "name": "La Terrace",
        "area": "Chundevi, Kathmandu",
        "description": (
            "A stylish garden-and-indoor restaurant in Chundevi — a calmer, less-known alternative to "
            "the busier café strips, good for a slow solo meal."
        ),
        "latitude": "27.735000", "longitude": "85.335000",
        "vibe_tags": ["peaceful", "cozy", "romantic"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="10:00", time_end="20:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Garden and indoor seating, relaxed pace, easy solo table"),
        ],
        "safety": [
            dict(category="transport",
                 content="15–20 min / Rs 300–500 by Pathao/inDrive from Thamel — normal paved city streets."),
            dict(category="area_safety",
                 content="A staffed restaurant in a quiet residential-commercial area — calm and comfortable solo.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Good 4G."),
            dict(category="local_attitude", content="Low-key, relaxed clientele."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Thamel, ~15–20 min.",
                 safe_until="20:30"),
        ],
        "stays": [],
    },
    {
        "name": "Bricks Cafe",
        "area": "Kupondole, Lalitpur",
        "description": (
            "A café in Kupondole with private, separated seating areas — a good option when you want "
            "a garden-cafe feel without being in the middle of a crowd, even at a fairly central location."
        ),
        "latitude": "27.690000", "longitude": "85.316000",
        "vibe_tags": ["peaceful", "cozy"],
        "solo_difficulty": 1,
        "min_comfort_tier": "first_timer",
        "budget_tier": "under_1000",
        "scene_type": "cafe_social",
        "windows": [
            dict(day_type="any", time_start="09:00", time_end="20:00",
                 crowd_level="low", solo_comfortable=True,
                 vibe_notes="Private, separated seating areas — genuinely calm despite the central location"),
        ],
        "safety": [
            dict(category="transport",
                 content="10–15 min / Rs 250–400 by Pathao/inDrive from Thamel or Patan — normal paved city streets."),
            dict(category="area_safety",
                 content="A staffed café on a busy but well-lit central road — calm and comfortable solo.",
                 safe_until="20:00"),
            dict(category="connectivity", content="Good 4G."),
            dict(category="local_attitude", content="Relaxed, low-hassle crowd."),
            dict(category="emergency",
                 content="Nepal Police 100 · Tourist Police 1144 · Women's helpline 1145 · Ambulance 102."),
            dict(category="return_route",
                 content="Ride-hailing works easily from the entrance.",
                 transport_back="Pathao/inDrive car back to Thamel or Patan, ~10–15 min.",
                 safe_until="20:30"),
        ],
        "stays": [],
    },
]
PLACES = PLACES + CAFE_PLACES


class Command(BaseCommand):
    help = "Seed real, researched Kathmandu Valley locations into Experience/SafetyIntel/VerifiedStay."

    @transaction.atomic
    def handle(self, *args, **options):
        created, updated = 0, 0
        for place in PLACES:
            exp, was_created = Experience.objects.update_or_create(
                name=place["name"], area=place["area"],
                defaults=dict(
                    description=place["description"],
                    latitude=place["latitude"],
                    longitude=place["longitude"],
                    vibe_tags=place["vibe_tags"],
                    solo_difficulty=place["solo_difficulty"],
                    min_comfort_tier=place["min_comfort_tier"],
                    budget_tier=place["budget_tier"],
                    scene_type=place.get("scene_type", "hidden_gem"),
                    best_months=place.get("best_months", []),
                    is_active=True,
                ),
            )
            created += was_created
            updated += not was_created

            exp.vibe_windows.all().delete()
            for w in place["windows"]:
                VibeWindow.objects.create(experience=exp, **w)

            exp.safety_intel.all().delete()
            for s in place["safety"]:
                SafetyIntel.objects.create(experience=exp, verified_date=VERIFIED_DATE, **s)

            exp.verified_stays.all().delete()
            for st in place.get("stays", []):
                VerifiedStay.objects.create(experience=exp, **st)

            self.stdout.write(f"  {'created' if was_created else 'updated'}: {exp.name} ({exp.area})")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created} experiences created, {updated} updated. "
            f"{len(PLACES)} Kathmandu Valley locations seeded."
        ))
