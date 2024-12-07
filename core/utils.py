"""
Core Utils
"""

import re
from core.config import EXCEPTIONS


def format_title(title: str) -> str:
    """
    Formats the text using camel case.
    """
    words: list[str] = title.split()
    formatted_title: list[str] = [
        word.capitalize() if word.lower() not in EXCEPTIONS else word.lower()
        for word in words
    ]
    formatted_title[0] = formatted_title[0].capitalize()
    return " ".join(formatted_title)


def extract_year(raw_text: str) -> str:
    """
    Extracts a year (4 digits) from a text.
    """
    match: re.Match[str] | None = re.search(r"\b\d{4}\b", raw_text)
    return match.group(0) if match else "Unknown"
