"""Defines the correct scrapers for urls."""

from urllib.parse import urlparse

from .allrecipes import AllRecipes

SCRAPERS = {
    AllRecipes.host_name()  :   AllRecipes
}

class UnknownWebsiteError(NotImplementedError):
    """Error for if a website has not been implemented yet."""

def parse(url):
    """Choose an appropriate scraper and scrape the url."""
    hostname = urlparse(url).hostname

    try:
        scraper = SCRAPERS[hostname]
    except KeyError:
        raise UnknownWebsiteError('No scraper for {}'.format(hostname))

    return _to_json(scraper(url))

def _to_json(scraper):
    """Convert valid scraper object to json."""
    results = {}

    results['host_name'] = scraper.host_name()
    results['title'] = scraper.title()
    results['summary'] = scraper.summary()
    results['instructions'] = scraper.instructions()
    results['image_url'] = scraper.image_url()
    results['time'] = scraper.time()
    results['ingredients'] = scraper.ingredients()

    return results
