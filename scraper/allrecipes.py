"""Provides concrete implementation for AllRecipes."""

import re
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

    def image_url(self):
        """Return the url of the main recipe image."""
        img_obj = self.soup.find(attrs={'class': 'photo-strip__items'}).find('li').find('img')
        img_src = img_obj['src']

        # img_src is thumbnail size. need to upscale it (allrecipes lets you pass in parameters through url)
        img_src = re.sub(r"/[0-9]+x[0-9]+/", "/600x600/", img_src)
        return img_src

    def time(self):
        """Return the total time to make in minutes."""
        time_raw = self.soup.find(attrs={'class': 'ready-in-time'}).text

        hour_match = re.search('([0-9]+) h', time_raw)
        minute_match = re.search('([0-9]+) m', time_raw)

        total_time = 0
        if hour_match:
            total_time += int(hour_match.group(1)) * 60
        if minute_match:
            total_time += int(minute_match.group(1))

        return str(total_time)
