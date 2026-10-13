"""
AI mode: asks Google Gemini to write a brand new excuse every time.

Needs a free Gemini API key (https://aistudio.google.com/apikey) saved as
GEMINI_API_KEY in .streamlit/secrets.toml (locally) or in the app's Secrets
on Streamlit Community Cloud. Without a key, the app falls back to the
built-in template excuses.
"""

import os
import random

import streamlit as st

DEFAULT_MODEL = "gemini-3.5-flash-lite"

# A random comedy angle is picked each time, so excuses don't all sound the same.
ANGLES = [
    "like a live cricket commentator calling the traffic ball by ball",
    "like a breaking news anchor reporting from the scene",
    "like a weather forecast, but for traffic",
    "like a nature documentary narrator observing the vehicles",
    "with an overly detailed minute-by-minute timeline",
    "like a very calm yoga teacher who has accepted their fate",
    "like a movie hero giving a dramatic dialogue",
    "like a product manager writing a status update",
    "like someone writing a heartfelt letter from a faraway land",
    "like a detective who has solved the mystery of why traffic exists",
    "like a travel blogger reviewing the jam as a tourist spot",
    "like a sports coach giving a pep talk to themselves",
    "with one surprising, oddly specific detail about something they can see from the vehicle",
    "like a philosopher wondering if they will ever arrive anywhere",
]

SYSTEM_INSTRUCTION = """You write funny "running late" text messages for people stuck in Bengaluru traffic.

Rules:
- Write ONLY the message itself, ready to paste into WhatsApp. No title, no quotes, no explanation.
- Keep it under 70 words. Start with a short greeting on its own line, then the message.
- Be clean, warm and witty. No swearing, nothing rude.
- Never make fun of any community, religion, region, language or group of people. Laugh at the traffic, the roads, the weather and the situation, not at people.
- Don't mention real people by name, except the recipient's name if one is given.
- Never suggest texting or using a phone while driving.
- Match the relationship: respectful for a boss, professor or client; casual for friends; sweet for a date; reassuring for parents.
- Mention the jam spot and include the realistic arrival time or delay you are given.
- Make it feel fresh. Don't reuse the jokes from the previous excuses you are shown."""


def get_api_key() -> str | None:
    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:  # no secrets file at all
        key = None
    return key or os.environ.get("GEMINI_API_KEY")


def get_model() -> str:
    try:
        model = st.secrets.get("GEMINI_MODEL")
    except Exception:
        model = None
    return model or os.environ.get("GEMINI_MODEL") or DEFAULT_MODEL


@st.cache_resource
def _client(api_key: str):
    from google import genai

    return genai.Client(api_key=api_key)


def write_excuse(
    *,
    hotspot: str,
    audience: str,
    name: str,
    tone: str,
    extras: list[str],
    timing: str,
    previous: list[str],
) -> str:
    """Ask Gemini for a fresh excuse. Raises an exception if anything goes wrong."""
    from google.genai import types

    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("No Gemini API key set.")

    angle = random.choice(ANGLES)
    bad_luck = ", ".join(e.split(" ", 1)[1] for e in extras) if extras else "none"
    recipient = name[:30].strip() or "no name given"
    previous_text = "\n---\n".join(previous[-3:]) if previous else "none yet"

    prompt = f"""Write a running-late message with these details:
- Stuck at: {hotspot}, Bengaluru
- Texting: {audience.split(' ')[0]} (name: {recipient})
- Vibe: {tone.split(' ', 1)[1]}{' (mix in a few simple, friendly Kannada words like guru, swalpa, ayyo, sakkat)' if 'Kannada' in tone else ''}
- Extra bad luck: {bad_luck}
- Timing to include: {timing}
- Comedy angle for this one: write it {angle}

Previous excuses (do not repeat these jokes):
{previous_text}"""

    response = _client(api_key).models.generate_content(
        model=get_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=1.2,
        ),
    )
    text = (response.text or "").strip().strip('"').strip()
    if not text:
        raise RuntimeError("Empty response from Gemini.")
    return text
