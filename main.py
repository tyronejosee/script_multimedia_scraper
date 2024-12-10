"""
Entrypoint
"""

import argparse
import logging
from typing import Any

from core import config
from core.logging import setup_logging
from modules.movie_scraper import MovieScraper
from modules.anime_scraper import AnimeScraper
from modules.music_scraper import MusicScraper
from modules.book_scraper import BookScraper

setup_logging()


SCRAPER_CONFIG = {
    "movie": {
        "scraper_class": MovieScraper,
        "headers": config.HEADERS_ES,
        "elements": config.MOVIES_ELEMENTS,
        "output_file": "movie_list.txt",
    },
    "serie": {
        "scraper_class": MovieScraper,
        "headers": config.HEADERS_EN,
        "elements": config.SERIES_ELEMENTS,
        "output_file": "movie_list.txt",
    },
    "anime": {
        "scraper_class": AnimeScraper,
        "headers": config.HEADERS_EN,
        "elements": config.ELEMENTS_TO_SCRAPE,
        "output_file": "anime_list.txt",
    },
    "music": {
        "scraper_class": MusicScraper,
        "headers": config.HEADERS_EN,
        "elements": None,
        "output_file": "music_list.txt",
    },
    "book": {
        "scraper_class": BookScraper,
        "headers": config.HEADERS_EN,
        "elements": config.BOOKS_ELEMENTS,
        "output_file": "book_list.txt",
    },
}


def read_links_from_file(file_path: str) -> list[str]:
    """
    Reads the links from a text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        logging.error(f"Error: file {file_path} was not found.")
        return []
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return []


def save_results_to_file(file_path: str, data: str):
    """
    Saves the scraped results to a text file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)


def execute_scraper(scraper_type: str, links: list[str]):
    """
    Executes the scraper based on the selected type.
    """
    config = SCRAPER_CONFIG.get(scraper_type)
    if not config:
        logging.error(f"Error: Invalid scraper type '{scraper_type}'.")
        return

    scraper_class: Any = config["scraper_class"]
    headers: dict[str, str] = config["headers"]
    elements: dict[str, str] = config["elements"]
    output_file: str = config["output_file"]

    scraper = scraper_class(headers=headers, elements=elements)
    results: str = scraper.scrape_links(links)
    save_results_to_file(output_file, results)
    logging.warning(f"Results saved to {output_file}")


if __name__ == "__main__":
    """
    Main function to execute the web scraping script.
    It reads the links from a file and scrapes the data
    based on the selected type (movie, anime, or music).
    The results are saved in separate output files.
    """
    links_file = "static/links.txt"
    links: list[str] = read_links_from_file(links_file)

    # Args configs
    parser = argparse.ArgumentParser(description="Webscrapping Script.")
    parser.add_argument(
        "--type",
        choices=["movie", "serie", "anime", "music", "book"],
        required=True,
        help="Select the type of scraper to run.",
    )
    args: argparse.Namespace = parser.parse_args()

    if not links:
        logging.error(f"No links found in {links_file}")
    else:
        logging.warning("Starting...")
        execute_scraper(args.type, links)
