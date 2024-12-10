"""
Core Configs.
"""

HEADERS_EN: dict[str, str] = {
    "Accept-Language": "en-US",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

HEADERS_ES: dict[str, str] = {
    "Accept-Language": "es-MX",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

EXCEPTIONS: set[str] = {
    "los",
    "las",
    "el",
    "la",
    "y",
    "de",
    "del",
    "para",
    "por",
    "en",
}

ROMAN_NUMERALS: set[str] = {
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
    "XIII",
    "XIV",
    "XV",
    "XVI",
    "XVII",
    "XVIII",
    "XIX",
    "XX",
}

ELEMENTS_TO_SCRAPE: dict[str, str] = {
    "title_jpn": "h1.title-name.h1_bold_none > strong",
    "title_eng": "div.h1-title > div > p.title-english.title-inherit",
    "year": "div.spaceit_pad:-soup-contains('Premiered:') a",
    "og_image": 'meta[property="og:image"]',
}

MOVIES_ELEMENTS: dict[str, str] = {
    "title": "h1 > span.hero__primary-text",
    "year": "div.sc-70a366cc-0.bxYZmb > ul.ipc-inline-list > li.ipc-inline-list__item",
}

SERIES_ELEMENTS: dict[str, str] = {
    "title": "h1 > span.hero__primary-text",
    "year": "div.sc-70a366cc-0.bxYZmb > ul.ipc-inline-list > li.ipc-inline-list__item > a.ipc-link",
}

BOOKS_ELEMENTS: dict[str, str] = {
    "title": "h1.Text.Text__title1",
    "year": "div.FeaturedDetails p[data-testid='publicationInfo']",
}
