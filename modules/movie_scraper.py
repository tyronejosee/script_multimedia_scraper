"""
Movie Scraper Module
"""

import requests
from requests import Response
from bs4 import BeautifulSoup, Tag

from .base_scraper import BaseScraper
# from core.utils import format_title


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
            url: str | None = data.get("url")
            title: str | None = data.get("title", "Not Title")
            year: str | None = data.get("year", "0000")

            # if title:
            #     title = format_title(title)

            return (
                f"\n# {title} ({year})\n\n"
                f"Registry: {url}\n"
                f"Link: <?>\n\n"
            )
        except Exception as e:
            print(f"Error {link}: {e}")
            return ""
