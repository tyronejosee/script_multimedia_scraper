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
                data[name] = element.text.strip() if element else ""

            # Extract the image
            image_tag: Tag | NavigableString | None = soup.find(
                "meta", property="og:image"
            )
            if isinstance(image_tag, Tag) and image_tag.get("content"):
                data["image"] = str(image_tag.get("content", ""))
            else:
                data["image"] = ""

            # Get each element from the dictionary
            title_eng: str | None = data.get("title_eng") or None
            title_jpn: str = data.get("title_jpn") or "Not Title"
            year: str = extract_year(data.get("year") or "0000")
            url: str = data.get("url") or ""
            image: str = data.get("image", "")

            title: str = (
                format_title(title_eng)
                if title_eng
                else format_title(title_jpn)
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
