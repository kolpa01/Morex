from .base import base


def label(text: str):
    base("\n\033[1;95m", text + "\n")
