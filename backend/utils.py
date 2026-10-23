# backend/utils.py
"""Utility functions for weather fetching and smart suggestions.
Only standard library and httpx are used; async functions are compatible with FastAPI.
"""
import time
import os
import json
import httpx
from . import config
from .db import get_db

_cached_weather = None
_cached_ts = 0
CACHE_TTL = 300  # seconds

async def fetch_weather():
    """Fetch current day weather (temp & rainfall) using OpenWeatherMap.
    Returns a dict matching WeatherResponse schema.
    """
    if not config.OPENWEATHER_API_KEY or not config.WEATHER_LAT or not config.WEATHER_LON:
        return {"temperature_c": 0.0, "rainfall_mm": 0.0, "description": "Weather data unavailable (missing env vars)"}
    global _cached_weather, _cached_ts
    now = time.time()
    if _cached_weather and now - _cached_ts < CACHE_TTL:
        return _cached_weather
    url = (
        f"https://api.openweathermap.org/data/2.5/onecall?lat={config.WEATHER_LAT}&lon={config.WEATHER_LON}"
        f"&exclude=minutely,hourly,alerts&units=metric&appid={config.OPENWEATHER_API_KEY}"
    )
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            today = data["daily"][0]
            temp = today["temp"]["day"]
            rain = today.get("rain", 0.0)
            desc = today["weather"][0]["description"]
            result = {"temperature_c": temp, "rainfall_mm": rain, "description": desc}
    except Exception as e:
        result = {"temperature_c": 0.0, "rainfall_mm": 0.0, "description": f"Weather fetch error: {e}"}
    _cached_weather = result
    _cached_ts = now
    return result

async def get_smart_suggestions():
    """Generate up to three rule‑based suggestions.
    Uses live weather and recent feedback trends.
    """
    suggestions = []
    weather = await fetch_weather()
    # Suggestion 1: rain forecast (any amount) triggers a check
    if weather["rainfall_mm"] > 0:
        suggestions.append("Rain is expected today. Check attendance before preparing the second batch of rice.")
    # Suggestion 2: recent high waste (placeholder logic)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT waste_rate_pct FROM feedback ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
    # If any recorded waste_rate_pct > 20, warn
    high_waste = any(row["waste_rate_pct"] > 20 for row in rows if row["waste_rate_pct"] is not None)
    if high_waste:
        suggestions.append("Recent meals have shown high leftovers. Consider reducing the initial batch size.")
    # Suggestion 3: uncertain demand (no recent attendance data placeholder)
    suggestions.append("Demand is uncertain today. Verify attendance estimates before finalizing the batch.")
    return suggestions[:3]
