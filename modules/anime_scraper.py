"""
Anime Scraper Module
"""

import requests
from bs4 import BeautifulSoup, Tag

from .base_scraper import BaseScraper
from core.utils import format_title, extract_year


class AnimeScraper(BaseScraper):
    """
    Scraper specialized in extracting anime data from a URL.
    """

    def scrape_link(self, link: str) -> str:
        try:
            response = requests.get(link, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            data: dict[str, str] = {"url": link}

            for name, selector in self.elements.items():
                element: Tag | None = soup.select_one(selector)
                data[name] = element.text.strip() if element else None

            # Extract the image
            image_tag = soup.find("meta", property="og:image")
            if image_tag and image_tag.get("content"):
                data["image"] = image_tag["content"]

            title_eng: str | None = data.get("title_eng")
            title_jpn: str | None = data.get("title_jpn")
            raw_year: str = data.get("year", "")

            year: str = extract_year(raw_year)
            title = format_title(title_eng) if title_eng else format_title(title_jpn)

            return (
                f"\n# {title} ({year})\n\n"
                f"Registry: {data['url']}\n"
                f"Image: {data['image']}\n"
                f"Link: <?>\n\n"
            )
        except Exception as e:
            print(f"Error {link}: {e}")
            return ""
