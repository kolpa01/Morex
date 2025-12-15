from .base import base


def success(text: str):
    base("\033[92m[SUCCESS] ", text)
