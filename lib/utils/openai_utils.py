import requests

from config import OPENAI_MODEL, OPENAI_KEY


def get_completions(completion_params: dict) -> dict:
    completion_params.setdefault("model", OPENAI_MODEL)
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_KEY}"},
        json=completion_params,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]
