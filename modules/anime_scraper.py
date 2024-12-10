"""
Anime Scraper Module
"""

import logging
import requests
from requests import Response
from bs4 import BeautifulSoup, NavigableString, Tag

from .base_scraper import BaseScraper
from core.logging import setup_logging
from core.utils import format_title, extract_year

setup_logging()


class AnimeScraper(BaseScraper):
    """
    Scraper specialized in extracting anime data from a URL.
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

            # Extract the image
            image_tag: Tag | NavigableString | None = soup.find(
                "meta", property="og:image"
            )
            if image_tag and image_tag.get("content"):
                data["image"] = image_tag["content"]

            # Get each element from the dictionary
            title_eng: str = data.get("title_eng", "")
            title_jpn: str = data.get("title_jpn", "")
            year: str = extract_year(data.get("year", ""))
            url: str = data.get("url")
            image: str = data.get("image", "")

            title: str = (
                format_title(title_eng) if title_eng else format_title(title_jpn)
            )

            logging.info(f"Processing: {title} ({year})")
            return (
                f"\n# {title} ({year})\n\n"
                f"Registry: {url}\n"
                f"Image: {image}\n"
                f"Link: <?>\n\n"
            )
        except Exception as e:
            logging.info(f"Error {link}: {e}")
            return ""
