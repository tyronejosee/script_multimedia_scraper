"""
Movie Scraper Module
"""

import requests
import logging
from requests import Response
from bs4 import BeautifulSoup, Tag

from .base_scraper import BaseScraper
from core.config import HEADERS_ES
from core.logging import setup_logging
from core.utils import extract_year, format_title

setup_logging()


class MovieScraper(BaseScraper):
    """
    Scraper specialized in extracting movie data from a URL.
    """

    def scrape_link(self, link: str) -> str:
        try:
            response: Response = requests.get(link, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            data: dict[str, str] = {"url": link}

            for name, selector in self.elements.items():
                element: Tag | None = soup.select_one(selector)
                data[name] = element.text.strip() if element else ""

            # Get each element from the dictionary
            url: str = data.get("url") or ""
            url = url.replace("/es", "")
            title: str = data.get("title") or "Not Title"
            year: str = extract_year(data.get("year") or "0000")

            if self.headers == HEADERS_ES:
                title = format_title(title)

            logging.info(f"Processing: {title} ({year})")
            return (
                f"\n# {title} ({year})\n\n"
                f"Registry: {url}\n"
                f"Link: <?>\n\n"
            )
        except Exception as e:
            logging.error(f"Error {link}: {e}")
            return ""
