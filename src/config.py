import os
from pathlib import Path

APP_DIR = Path(__file__).parent.parent
SRC_DIR = APP_DIR.joinpath("src")
CACHE_DIR = APP_DIR.joinpath("cache")
LOG_DIR = CACHE_DIR.joinpath("logs")
BOOKS_DIR = SRC_DIR.joinpath("books")
BOOKS_GENERATED_DIR = SRC_DIR.joinpath("books_generated")

DICT_ENDPOINT = os.getenv("DICT_ENDPOINT")
AUDIO_ENDPOINT = os.getenv("AUDIO_ENDPOINT")
DICT_API_KEY = os.getenv("DICT_API_KEY")

DB_HOST = os.getenv("DB_HOST", "192.168.1.110")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "readin")
DB_PORT = os.getenv("DB_PORT", 3306)

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_KEY = os.getenv("OPENAI_KEY")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
HOME_NEWS_NUM = os.getenv("HOME_NEWS_NUM", 3)

STATIC_VERSION = os.getenv("STATIC_VERSION", "1")
