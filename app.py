import random
from datetime import datetime, timedelta
from urllib.parse import quote
from zoneinfo import ZoneInfo

import streamlit as st

from ai import get_api_key, write_excuse
from excuses import AUDIENCES, EXTRAS, HOTSPOTS, TIME_SLOTS, TONES

IST = ZoneInfo("Asia/Kolkata")
RIGHT_NOW = "Right now (auto)"
MAX_AI_PER_SESSION = 20  # protects your free Gemini quota from one person spamming the button


# ---------- helpers ----------

def clock(t: datetime) -> str:
    """9:05 PM style time that works on Windows, Mac and Linux."""
    return t.strftime("%I:%M %p").lstrip("0")


def slot_for_hour(hour: int) -> str:
    """Pick the time slot that matches the current hour."""
    if 5 <= hour < 8:
        return "Early morning (5–8 AM)"
    if 8 <= hour < 11:
        return "Morning rush (8–11 AM)"
    if 11 <= hour < 16:
        return "Afternoon (11 AM–4 PM)"
    if 16 <= hour < 21:
        return "Evening rush (4–9 PM)"
    if 21 <= hour < 24:
        return "Night (9 PM–12 AM)"
    return "Late night (12–5 AM)"


def nice_minutes(mins: int) -> str:
    if mins < 60:
        return f"{mins} min"
    hours, rest = divmod(mins, 60)
    return f"{hours} hr {rest} min" if rest else f"{hours} hr"


def estimate(hotspot: str, distance_km: float, slot: str, extras: list[str]) -> tuple[int, int]:
    """Return (what Google Maps promises, what Bengaluru actually delivers) in minutes."""
    spot = HOTSPOTS[hotspot]
    time_info = TIME_SLOTS[slot]

    maps_mins = round(distance_km / 25 * 60) + 2

    # The jam spot itself is crawl speed for ~2 km; the rest of the trip is normal city traffic.
    jam_km = min(distance_km, 2)
    rest_km = distance_km - jam_km
    jam_speed = spot["speed"] * time_info["speed"]
    city_speed = 20 * time_info["speed"]
    stuck = spot["stuck"] * time_info["stuck"]
    for name in extras:
        jam_speed *= EXTRAS[name]["speed"]
        city_speed *= EXTRAS[name]["speed"]
        stuck += EXTRAS[name]["extra"]
    jam_speed = max(jam_speed, 2)  # even Silk Board moves a little
    city_speed = max(city_speed, 5)

    real_mins = round(jam_km / jam_speed * 60 + rest_km / city_speed * 60 + stuck)
    return maps_mins, max(real_mins, maps_mins + 1)


def believability(hotspot: str, slot: str, extras: list[str]) -> tuple[int, str]:
    """Score how believable the excuse is, with a warning if something smells fishy."""
    score = HOTSPOTS[hotspot]["fame"]
    warning = ""

    if slot in ("Late night (12–5 AM)", "Night (9 PM–12 AM)") and not extras:
        score -= 35
        warning = f"Nobody believes {hotspot} traffic at this hour. Add some bad luck or leave earlier."
    elif slot == "Early morning (5–8 AM)" and not extras:
        score -= 20
        warning = "Traffic this early? Bold claim. A bus breakdown or a cow might help."

    if len(extras) >= 3:
        score -= 15 * (len(extras) - 2)
        warning = "That's a lot of bad luck for one trip. Very suspicious. 🤨"

    return max(5, min(99, score)), warning


def verdict(score: int) -> str:
    if score >= 85:
        return "Airtight. Even the person you're texting has been stuck there."
    if score >= 60:
        return "Believable. Send it with confidence."
    if score >= 35:
        return "Risky. Attach a photo of the traffic as proof."
    return "Nobody is buying this. Maybe just leave earlier next time 😅"


def build_message(rng, hotspot, audience, name, tone, extras, real_mins, eta_clock):
    aud = AUDIENCES[audience]
    tone_info = TONES[tone]

    greeting = aud["greeting"].format(name=name).replace(" ,", ",").strip()
    if not greeting.endswith((",", "!")):
        greeting += ","

    parts = [greeting]
    intro = rng.choice(tone_info["intros"])
    if intro:
        parts.append(intro)
    parts.append(rng.choice(HOTSPOTS[hotspot]["lines"]))
    for name_ in extras:
        parts.append(rng.choice(EXTRAS[name_]["lines"]))

    if eta_clock:
        parts.append(f"Realistically, I'll be there by around {eta_clock}.")
    else:
        parts.append(f"Realistically, I'm still about {nice_minutes(real_mins)} away.")

    parts.append(rng.choice(aud["closers"]))
    outro = rng.choice(tone_info["outros"])
    if outro:
        parts.append(outro)

    # Greeting on its own line, rest as one paragraph
    return parts[0] + "\n\n" + " ".join(parts[1:])


# ---------- page ----------

st.set_page_config(page_title="Bengaluru Traffic Excuse Generator", page_icon="🚦", layout="centered")

defaults = {
    "seed": random.randint(0, 1_000_000),
    "ai_message": "",
    "ai_settings": None,
    "ai_history": [],
    "ai_count": 0,
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)

st.title("🚦 Bengaluru Traffic Excuse Generator")
st.caption("Because \"5 minutes away\" stopped working years ago.")

col1, col2 = st.columns(2)
with col1:
    hotspot = st.selectbox(
        "Where are you stuck?",
        list(HOTSPOTS.keys()),
        format_func=lambda h: f"{HOTSPOTS[h]['emoji']} {h}",
    )
    audience = st.selectbox("Who are you texting?", list(AUDIENCES.keys()))
    name = st.text_input(
        "Their name (optional)",
        key="their_name",
        placeholder=AUDIENCES[audience]["default_name"] or "e.g. Priya",
    )
with col2:
    distance = st.slider("How far are you still? (km)", 1, 30, 8)
    slot_choice = st.selectbox("When is this?", [RIGHT_NOW, *TIME_SLOTS.keys()])
    tone = st.radio("Pick a vibe", list(TONES.keys()), horizontal=True)

extras = st.pills("Add some extra bad luck", list(EXTRAS.keys()), selection_mode="multi") or []

# Work out the time slot and ETA
now = datetime.now(IST)
slot = slot_for_hour(now.hour) if slot_choice == RIGHT_NOW else slot_choice
maps_mins, real_mins = estimate(hotspot, distance, slot, extras)
eta_clock = clock(now + timedelta(minutes=real_mins)) if slot_choice == RIGHT_NOW else ""

display_name = name.strip() or AUDIENCES[audience]["default_name"]

# ---------- AI mode ----------
ai_ready = get_api_key() is not None
use_ai = st.toggle(
    "✨ AI mode: a brand new excuse every time",
    value=ai_ready,
    disabled=not ai_ready,
    help="Uses Google Gemini to write a fresh excuse each time you press the button.",
)
if not ai_ready:
    st.caption("AI mode is off because no Gemini API key is set. See the README to turn it on (it's free).")

settings = (hotspot, audience, name, tone, tuple(extras), distance, slot_choice)
clicked = st.button(
    "✨ Write me a fresh excuse" if use_ai else "🔄 Give me another excuse",
    type="primary",
    use_container_width=True,
)

ai_failed = False
if clicked:
    st.session_state.seed = random.randint(0, 1_000_000)
    if use_ai:
        if st.session_state.ai_count >= MAX_AI_PER_SESSION:
            st.warning("You've used up the AI excuses for this session. Here's a classic one instead. 😅")
            ai_failed = True
        else:
            timing = (
                f"will reach around {eta_clock} (about {nice_minutes(real_mins)} from now)"
                if eta_clock
                else f"still about {nice_minutes(real_mins)} away"
            )
            try:
                with st.spinner("The AI is also stuck in traffic. One sec..."):
                    fresh = write_excuse(
                        hotspot=hotspot,
                        audience=audience,
                        name=name,
                        tone=tone,
                        extras=extras,
                        timing=timing,
                        previous=st.session_state.ai_history,
                    )
                st.session_state.ai_message = fresh
                st.session_state.ai_settings = settings
                st.session_state.ai_history.append(fresh)
                st.session_state.ai_count += 1
            except Exception:
                st.info("The AI is on a chai break right now (busy or out of free requests). Here's a classic one instead. ☕")
                ai_failed = True

rng = random.Random(st.session_state.seed)
template_message = build_message(rng, hotspot, audience, display_name, tone, extras, real_mins, eta_clock)

if use_ai and not ai_failed and st.session_state.ai_message:
    message = st.session_state.ai_message
    if st.session_state.ai_settings != settings:
        st.caption("You changed the settings. Press ✨ for an excuse that matches.")
else:
    message = template_message
    if use_ai and not ai_failed:
        st.caption("Press ✨ for an AI-written excuse. Meanwhile, here's a classic one.")

st.subheader("Your excuse 📱")
st.code(message, language=None, wrap_lines=True)

st.link_button(
    "💬 Send on WhatsApp",
    f"https://wa.me/?text={quote(message)}",
    use_container_width=True,
)

# Stats
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Google Maps says", nice_minutes(maps_mins))
m2.metric("Bengaluru says", nice_minutes(real_mins))
m3.metric("Reality check", f"{real_mins / maps_mins:.1f}x slower")

if slot_choice == RIGHT_NOW:
    st.caption(f"Using the current time in Bengaluru: {clock(now)} ({slot.split(' (')[0].lower()}).")

score, warning = believability(hotspot, slot, extras)
st.markdown(f"**Believability meter: {score}%**")
st.progress(score / 100)
st.write(verdict(score))
if warning:
    st.warning(warning)

st.divider()
st.caption(
    "Made for fun. If you're the one driving, let someone else send this. 🙏  \n"
    "Travel times are a joke formula, not real traffic data."
)
