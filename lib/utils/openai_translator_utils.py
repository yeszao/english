import requests
from lib.utils.openai_utils import get_completions


class ChatGptTranslator:
    def __init__(self, book_name: str):
        self.messages = [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "assistant",
                "content": f"Input a sentence from book {book_name}."
            },

            {
                "role": "user",
                "content": ""
            }
        ]

    def translate(self, text: str, lang: str) -> str:
        self.messages[0]["content"] = f"Please translate the sentence to langauge {lang}."
        self.messages[-1]["content"] = text

        return get_completions({"messages": self.messages})["message"]["content"]


if __name__ == '__main__':
    translator = ChatGptTranslator("The Great Gatsby")
    print(translator.translate("In consequence I’m inclined to reserve all judgments", "zh-cn"))
