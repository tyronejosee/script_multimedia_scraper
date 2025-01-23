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
            response: Response = requests.get(link, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            data: dict[str, str] = {"url": link}

            # Extract title
            title_tag: Tag | NavigableString | None = soup.find("title")
            if title_tag:
                title_text: str = title_tag.text.strip()
                if " - " in title_text:
                    album_name, artist_name = title_text.split(" - ", 1)
                    data["album"] = album_name.strip()
                    artist_name: str = (
                        re.sub(r"^Album by\s*", "", artist_name)
                        .replace(" | Spotify", "")
                        .strip()
                    )
                    data["artist"] = artist_name

            json_data = {}
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    info: dict = json.loads(script.string)
                    if info.get("@type") == "MusicAlbum":
                        json_data: dict = info
                        break
                except json.JSONDecodeError:
                    continue

            # Extract year
            if json_data:
                data["year"] = json_data.get("datePublished", "").split("-")[0]

            # Extract the image
            image_tag: Tag | NavigableString | None = soup.find(
                "meta", property="og:image"
            )
            if isinstance(image_tag, Tag) and image_tag.get("content"):
                data["image"] = str(image_tag.get("content", ""))
            else:
                data["image"] = ""

            # Get each element from the dictionary
            artist: str = data.get("artist") or "Not Artist"
            album: str = data.get("album") or "Not Album"
            year: str = data.get("year") or "0000"
            image: str = data.get("image") or "Not Image"
            url: str = data.get("url") or "Not URL"

            logging.info(f"Processing: {artist} - {album} ({year})")
            return (
                f"\n# {artist} - {album} ({year})\n\n"
                f"Image: {image}\n"
                f"Link: <{url}>\n\n"
            )
        except Exception as e:
            logging.error(f"Error {link}: {e}")
            return ""
