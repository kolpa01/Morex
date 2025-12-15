from .base import base


def error(text: str):
    base("\033[1;91m", text)
