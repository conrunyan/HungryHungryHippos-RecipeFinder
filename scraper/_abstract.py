"""Provides the abstract definition for a scraper."""

from bs4 import BeautifulSoup
from urllib.request import urlopen

class AbstractScraper:
    """Defines the abstract recipe scraper."""

    def __init__(self, url):
        """Create a scraper from the given url."""
        self.url = url

        content = urlopen(url).read()
        self.soup = BeautifulSoup(content, "html.parser")


    def host_name(self):
        """Return the host name of the scraper."""
        raise NotImplementedError("abstract")
