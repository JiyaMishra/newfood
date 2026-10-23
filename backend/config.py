import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
load_dotenv(BASE_DIR / '.env')

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
WEATHER_LAT = os.getenv('WEATHER_LAT')
WEATHER_LON = os.getenv('WEATHER_LON')
