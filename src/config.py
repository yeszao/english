import os
from pathlib import Path

APP_DIR = Path(__file__).parent.parent
SRC_DIR = APP_DIR.joinpath("src")
CACHE_DIR = APP_DIR.joinpath("cache")
BOOKS_DIR = SRC_DIR.joinpath("books")
BOOKS_GENERATED_DIR = SRC_DIR.joinpath("books_generated")

DICT_ENDPOINT = os.getenv("DICT_ENDPOINT")
AUDIO_ENDPOINT = os.getenv("AUDIO_ENDPOINT")
DICT_API_KEY = os.getenv("DICT_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_KEY = os.getenv("OPENAI_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSDATA_KEY = os.getenv("NEWSDATA_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

STATIC_VERSION = os.getenv("STATIC_VERSION", "1")
