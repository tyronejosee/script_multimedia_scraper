"""
Base Scraper
"""


class BaseScraper:
    """
    Base class for web scraping functionality.
    Provides common methods and attributes to be extended by specific scrapers.
    """

    def __init__(
        self,
        headers: dict[str, str],
        elements: dict[str, str] = None,
    ):
        self.headers: dict[str, str] = headers
        self.elements: dict[str, str] = elements or {}

    def scrape_link(self, link: str) -> str:
        """
        Scrapes a specific link.
        """
        pass

    def scrape_links(self, links: list[str]) -> str:
        """
        Scrapes multiple links.
        """
        results: list[str] = [self.scrape_link(link) for link in links]
        return f"{'-' * 3}\n".join(results)
