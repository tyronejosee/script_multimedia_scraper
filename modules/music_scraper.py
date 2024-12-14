"""
Music Scraper Module
"""

import re
import json
import requests
import logging
from requests import Response
from bs4 import BeautifulSoup, NavigableString, Tag

from .base_scraper import BaseScraper
from core.logging import setup_logging

setup_logging()


class MusicScraper(BaseScraper):
    """
    Scraper specialized in extracting music data from a URL.
    """

    def scrape_link(self, link: str) -> str:
        try:
            # Perform an HTTP GET request to the provided URL
            response: Response = requests.get(link, headers=self.headers)
            response.raise_for_status()

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")
            scraped_row = {"URL": link}

            # Extract title
            title_tag = soup.find("title")
            if title_tag:
                title_text = title_tag.text.strip()
                if " - " in title_text:
                    album_name, artist_name = title_text.split(" - ", 1)
                    scraped_row["Album"] = album_name.strip()
                    artist_name = (
                        re.sub(r"^Album by\s*", "", artist_name)
                        .replace(" | Spotify", "")
                        .strip()
                    )
                    scraped_row["Artist"] = artist_name

            json_data = None
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string)
                    if data.get("@type") == "MusicAlbum":
                        json_data = data
                        break
                except json.JSONDecodeError:
                    continue

            # Extract year
            if json_data:
                scraped_row["Year"] = json_data.get("datePublished", "").split("-")[0]

            # Extract image
            image_tag = soup.find("meta", property="og:image")
            if image_tag and image_tag.get("content"):
                scraped_row["Image"] = image_tag["content"]

            # Get each element from the dictionary
            artist: str = scraped_row.get("Artist", "Not Artist")
            album: str = scraped_row.get("Album", "Not Album")
            year: str = scraped_row.get("Year", "0000")
            image: str = scraped_row.get("Image", "Not Image")
            url: str = scraped_row.get("URL", "Not URL")

            logging.info(f"Processing: {artist} - {album} ({year})")
            return (
                f"\n# {artist} - {album} ({year})\n\n"
                f"Image: {image}\n"
                f"Link: <{url}>\n\n"
            )
        except Exception as e:
            logging.error(f"Error {link}: {e}")
            return ""
