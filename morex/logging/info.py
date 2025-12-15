from .base import base


def info(text: str):
    base("\033[0;94m[INFO] ", text)
