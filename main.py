"""
Entrypoint
"""

import argparse

from modules.movie_scraper import MovieScraper
from modules.anime_scraper import AnimeScraper
from modules.music_scraper import MusicScraper
from modules.book_scraper import BookScraper
from core.config import (
    HEADERS_EN,
    HEADERS_ES,
    ELEMENTS_TO_SCRAPE,
    MOVIES_ELEMENTS,
    SERIES_ELEMENTS,
    BOOKS_ELEMENTS,
)


def read_links_from_file(file_path: str) -> list[str]:
    """
    Reads the links from a text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: file {file_path} was not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def save_results_to_file(file_path: str, data: str):
    """
    Saves the scraped results to a text file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)


if __name__ == "__main__":
    """
    Main function to execute the web scraping script.
    It reads the links from a file and scrapes the data
    based on the selected type (movie, anime, or music).
    The results are saved in separate output files.
    """
    links_file = "static/links.txt"
    links: list[str] = read_links_from_file(links_file)

    parser = argparse.ArgumentParser(description="Webscrapping Script.")
    parser.add_argument(
        "--movie",
        action="store_true",
        help="Movie Version",
    )
    parser.add_argument(
        "--serie",
        action="store_true",
        help="Serie Version",
    )
    parser.add_argument(
        "--anime",
        action="store_true",
        help="Anime Version",
    )
    parser.add_argument(
        "--music",
        action="store_true",
        help="Music Version",
    )
    parser.add_argument(
        "--book",
        action="store_true",
        help="Music Version",
    )
    args: argparse.Namespace = parser.parse_args()

    if args.movie:
        output_file = "movie_list.txt"
        scraper = MovieScraper(
            headers=HEADERS_ES,
            elements=MOVIES_ELEMENTS,
        )
        results: str = scraper.scrape_links(links)
        save_results_to_file(output_file, results)
    if args.serie:
        output_file = "serie_list.txt"
        scraper = MovieScraper(
            headers=HEADERS_EN,
            elements=SERIES_ELEMENTS,
        )
        results: str = scraper.scrape_links(links)
        save_results_to_file(output_file, results)
    elif args.anime:
        output_file = "anime_list.txt"
        scraper = AnimeScraper(
            headers=HEADERS_EN,
            elements=ELEMENTS_TO_SCRAPE,
        )
        results: str = scraper.scrape_links(links)
        save_results_to_file(output_file, results)
    elif args.music:
        output_file = "music_list.txt"
        scraper = MusicScraper(headers=HEADERS_EN)
        results: str = scraper.scrape_links(links)
        save_results_to_file(output_file, results)
    elif args.book:
        output_file = "book_list.txt"
        scraper = BookScraper(
            headers=HEADERS_EN,
            elements=BOOKS_ELEMENTS,
        )
        results: str = scraper.scrape_links(links)
        save_results_to_file(output_file, results)
    else:
        print("Error")
