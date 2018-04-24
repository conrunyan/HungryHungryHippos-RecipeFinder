"""Defines the correct scrapers for urls."""

from urllib.parse import urlparse

from .allrecipes import AllRecipes
from .errors import UnknownWebsiteError

SCRAPERS = {
    AllRecipes.host_name()  :   AllRecipes
}

def parse(url):
    """Choose an appropriate scraper and scrape the url."""
    scraper = _get_scraper(url)

    return _to_json(scraper(url))

def get_batch(base_url, start, end):
    """Return a list of urls appropriate to the parameters."""
    scraper = _get_scraper(base_url)

    sites = []
    for i in range(start, end + 1):
        sites.append(scraper.generate_url(i))
    return sites

def _get_scraper(url):
    """Return an appropriate scraper for the url."""
    hostname = urlparse(url).hostname

    try:
        scraper = SCRAPERS[hostname]
        return scraper
    except KeyError:
        raise UnknownWebsiteError('No scraper for {}'.format(hostname))

def _to_json(scraper):
    """Convert valid scraper object to json."""
    results = {}

    results['host_name'] = scraper.host_name()
    results['title'] = scraper.title()
    results['summary'] = scraper.summary()
    results['difficulty'] = scraper.difficulty()
    results['instructions'] = scraper.instructions()
    results['image_url'] = scraper.image_url()
    results['time'] = scraper.time()
    results['ingredients'] = scraper.ingredients()
    results['appliances'] = scraper.appliances()

    return results
