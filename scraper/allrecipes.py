"""Provides concrete implementation for AllRecipes."""

from ._abstract import AbstractScraper

class AllRecipes(AbstractScraper):
    """Defines the concrete scraper for AllRecipes."""

    @classmethod
    def host_name(self):
        """Return the host name for AllRecipes."""
        return "www.allrecipes.com"

    def title(self):
        """Return the title of the recipe."""
        return self.soup.find(attrs={'class': 'recipe-summary__h1'}).text

    def summary(self):
        """Return the short summary of the recipe."""
        return self.soup.find(attrs={'class': 'submitter__description'}).text

    def instructions(self):
        """Return the instructions of the recipe."""
        instructions = self.soup.find(attrs={'class': 'recipe-directions__list'})
        instruction_list = instructions.findAll('span')

        results = '<ol>'
        for item in instruction_list:
            results += '<li>{}</li>'.format(item.text)
        results += '</ol>'

        return results
