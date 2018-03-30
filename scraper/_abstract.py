"""Provides the abstract definition for a scraper."""

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# Supply user agent so scraper is not viewed as bot.
HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'
}

class AbstractScraper:
    """Defines the abstract recipe scraper."""

    def __init__(self, url, test=False):
        """Create a scraper from the given url. If test=True, then the url is the actual html."""
        self.url = url

        content = url
        if not test:
            contentFile = urlopen(Request(url, headers=HEADERS))
            content = contentFile.read()
            contentFile.close()
        self.soup = BeautifulSoup(content, "html.parser")

    def generate_url(self, number):
        """Generate a url with the specified parameters."""
        raise NotImplementedError("abstract")

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

    def ingredients(self):
        """Return the ingredients, amounts, and units needed to make the recipe."""
        raise NotImplementedError("abstract")

    def appliances(self):
        """Return the appliances needed to make the recipe."""
        raise NotImplementedError("abstract")
