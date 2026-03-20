import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "app.db"
EXPORTS_DIR = DATA_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

HH_BASE_URL = "https://api.hh.ru"
HH_USER_AGENT = "HH-Analytics-App/3.0"

GENAPI_API_KEY = "sk-vxqwOVCM3RudJqOLK1akWIYZg0CABEinB5SQuZNyOrqrl5EiaZ69aWRhZdnW"
GENAPI_BASE_URL = "https://openrouter.ai/api/v1"
GENAPI_MODEL = "GENAPI_MODEL", "gpt-4o-mini"

MAX_AI_VACANCIES = 20
REQUEST_TIMEOUT = 15
DEFAULT_PER_PAGE = 100
MAX_PAGES = 5
