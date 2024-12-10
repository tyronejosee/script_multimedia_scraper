"""
Music Scraper Module
"""

import re
import json
import requests
from requests import Response
from bs4 import BeautifulSoup, NavigableString, Tag

from .base_scraper import BaseScraper


class MusicScraper(BaseScraper):
    """
    Scraper specialized in extracting music data from a URL.
    """

    def scrape_link(self, link: str) -> str:
        try:
            response: Response = requests.get(
                link,
                headers=self.headers,
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            data: dict[str, str] = {"url": link}

            title_tag: Tag | NavigableString | None = soup.find("title")
            if title_tag:
                title_text = title_tag.text.strip()
                if " - " in title_text:
                    album_name, artist_name = title_text.split(" - ", 1)
                    data["album"] = album_name.strip()
                    artist_name = (
                        re.sub(r"^Album by\s*", "", artist_name)
                        .replace(" | Spotify", "")
                        .strip()
                    )
                    data["artist"] = artist_name

            json_data = None
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string)
                    if data.get("@type") == "MusicAlbum":
                        json_data = data
                        break
                except json.JSONDecodeError:
                    continue

            if json_data:
                data["year"] = json_data.get("datePublished", "").split("-")[0]

            image_tag: Tag | NavigableString | None = soup.find(
                "meta", property="og:image"
            )
            if image_tag and image_tag.get("content"):
                data["image"] = image_tag["content"]

            return (
                f"\n# {data['artist']} - {data['album']} ({data['year']})\n\n"
                f"Image: {data['image']}\n"
                f"Link: <{data['url']}>\n\n"
            )
        except Exception as e:
            print(f"Error {link}: {e}")
            return ""
