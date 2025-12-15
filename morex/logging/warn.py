from .base import base


def warn(text: str):
    base("\033[93m[WARN] ", text)
