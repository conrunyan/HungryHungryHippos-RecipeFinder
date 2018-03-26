"""Defines the correct scrapers for urls."""

from urllib.parse import urlparse

from .allrecipes import AllRecipes
from .errors import UnknownWebsiteError

SCRAPERS = {
    AllRecipes.host_name()  :   AllRecipes
}

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
    results['appliances'] = scraper.appliances()

    return results
