"""
Book Scraper Module
"""

import requests
import logging
from requests import Response
from bs4 import BeautifulSoup, NavigableString, Tag

from .base_scraper import BaseScraper
from core.logging import setup_logging
from core.utils import extract_year, format_title

setup_logging()


class BookScraper(BaseScraper):
    """
    Scraper specialized in extracting book data from a URL.
    """

    def scrape_link(self, link: str) -> str:
        try:
            # Perform an HTTP GET request to the provided URL
            response: Response = requests.get(link, headers=self.headers)
            response.raise_for_status()

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")
            data: dict[str, str] = {"url": link}

            # Iterate over selectors and extract their text
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
            title: str = format_title(data.get("title", "Not Title"))
            year: str = extract_year(data.get("year", "Not Year"))
            url: str = data.get("url", "Not URL")
            image: str = data.get("image", "Not Image")

            logging.info(f"Processing: {title} ({year})")
            return (
                f"\n# {title} ({year})\n\n"
                f"Registry: <{url}>\n"
                f"Image: {image}\n"
                f"Link: <?>\n\n"
            )
        except Exception as e:
            print(f"Error {link}: {e}")
            return ""
