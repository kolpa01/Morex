from .base import base


def critical(text: str):
    base("\033[38;2;255;255;255m\033[101m[FAIL] ", text)
