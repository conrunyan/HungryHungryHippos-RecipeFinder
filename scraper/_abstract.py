"""Provides the abstract definition for a scraper."""

from bs4 import BeautifulSoup
from urllib.request import urlopen

class AbstractScraper:
    """Defines the abstract recipe scraper."""

    def __init__(self, url):
        """Create a scraper from the given url."""
        self.url = url

        contentFile = urlopen(url)
        content = contentFile.read()
        contentFile.close()
        self.soup = BeautifulSoup(content, "html.parser")

    def source_url(self):
        """Return the url we are scraping from."""
        return self.url

    def host_name(self):
        """Return the host name of the scraper."""
        raise NotImplementedError("abstract")

    def title(self):
        """Return the title of the recipe."""
        raise NotImplementedError("abstract")

    def summary(self):
        """Return the short summary of the recipe."""
        return ''

    def instructions(self):
        """Return the instructions of the recipe."""
        raise NotImplementedError("abstract")

    def image_url(self):
        """Return the url of the main recipe image."""
        return ''

    def time(self):
        """Return the total time to make in minutes."""
        return ''
