"""
Movie Scraper Module
"""

import requests
import logging
from requests import Response
from bs4 import BeautifulSoup, Tag

from .base_scraper import BaseScraper
from core.config import HEADERS_ES
from core.utils import extract_year, format_title

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


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
                data[name] = element.text.strip() if element else None

            # Get each element from the dictionary
            url: str = data.get("url")
            title: str = data.get("title", "Not Title")
            year: str = extract_year(data.get("year", "0000"))

            if self.headers == HEADERS_ES:
                title = format_title(title)

            logging.info(f"Processing: {title} ({year})")
            return (
                f"\n# {title} ({year})\n\n"
                f"Registry: {url}\n"
                f"Link: <?>\n\n"
            )
        except Exception as e:
            print(f"Error {link}: {e}")
            return ""
