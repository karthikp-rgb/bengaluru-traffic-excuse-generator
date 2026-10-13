"""
Live data: real traffic speed at the jam spot (TomTom) and current
Bengaluru weather (Open-Meteo).

- TomTom needs a free API key (20,000 free requests a month, no card):
  https://developer.tomtom.com  ->  save it as TOMTOM_API_KEY in secrets.
- Open-Meteo is free and needs no key.

Both are cached for a few minutes so the app doesn't burn through the free
quota, and both return None if anything goes wrong, so the app falls back
to the joke formula instead of crashing.
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import streamlit as st

IST = ZoneInfo("Asia/Kolkata")
TOMTOM_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
BENGALURU = (12.9716, 77.5946)

# WMO weather codes that mean rain, showers or thunderstorms
RAIN_CODES = set(range(51, 68)) | set(range(80, 83)) | set(range(95, 100))


def get_tomtom_key() -> str | None:
    try:
        key = st.secrets.get("TOMTOM_API_KEY")
    except Exception:  # no secrets file at all
        key = None
    return key or os.environ.get("TOMTOM_API_KEY")


@st.cache_data(ttl=600, show_spinner=False)  # 10 minutes per jam spot
def _fetch_traffic(lat: float, lon: float, key: str) -> dict | None:
    try:
        r = requests.get(
            TOMTOM_URL,
            params={"key": key, "point": f"{lat},{lon}", "unit": "KMPH"},
            timeout=6,
        )
        r.raise_for_status()
        d = r.json()["flowSegmentData"]
        current = float(d["currentSpeed"])
        free_flow = max(float(d["freeFlowSpeed"]), current, 1.0)
        return {
            "current_speed": round(current),
            "free_flow_speed": round(free_flow),
            "ratio": max(0.05, min(1.0, current / free_flow)),
            "road_closed": bool(d.get("roadClosure", False)),
            "confidence": float(d.get("confidence", 1)),
            "fetched_at": datetime.now(IST),
        }
    except Exception:
        return None


def live_traffic(coords: tuple[float, float]) -> dict | None:
    """Live speed at a spot, or None if there's no key or the request fails."""
    key = get_tomtom_key()
    if not key:
        return None
    return _fetch_traffic(coords[0], coords[1], key)


@st.cache_data(ttl=900, show_spinner=False)  # 15 minutes
def bengaluru_weather() -> dict | None:
    """Current Bengaluru weather, or None if the request fails."""
    try:
        r = requests.get(
            WEATHER_URL,
            params={
                "latitude": BENGALURU[0],
                "longitude": BENGALURU[1],
                "current": "temperature_2m,precipitation,weather_code",
                "timezone": "Asia/Kolkata",
            },
            timeout=6,
        )
        r.raise_for_status()
        cur = r.json()["current"]
        code = int(cur.get("weather_code", 0))
        rain_mm = float(cur.get("precipitation", 0) or 0)
        return {
            "temp": round(float(cur["temperature_2m"])),
            "raining": code in RAIN_CODES or rain_mm > 0.1,
        }
    except Exception:
        return None


def jam_level(ratio: float) -> str:
    if ratio < 0.35:
        return "Severe 🔴"
    if ratio < 0.6:
        return "Heavy 🟠"
    if ratio < 0.85:
        return "Moderate 🟡"
    return "Clear 🟢"
