"""Provides concrete implementation for AllRecipes."""

import re
from ._abstract import AbstractScraper, HEADERS
from .string_utils import normalize
from .errors import IngredientParsingError, RecipeParsingError
from urllib.request import build_opener, Request, urlopen

class AllRecipes(AbstractScraper):
    """Defines the concrete scraper for AllRecipes."""

    @classmethod
    def generate_url(self, number):
        """Generate a url with the specified parameters."""
        url = "https://www.allrecipes.com/recipe/{}".format(number)
        # content = urlopen(Request(url, headers=HEADERS))
        # return content.geturl()
        return url

    @classmethod
    def host_name(self):
        """Return the host name for AllRecipes."""
        return "www.allrecipes.com"

    def title(self):
        """Return the title of the recipe."""
        title = self.soup.find(attrs={'class': 'recipe-summary__h1'})
        if not title:
            raise RecipeParsingError("No title found")
        return normalize(title.text)

    def summary(self):
        """Return the short summary of the recipe."""
        summary = self.soup.find(attrs={'class': 'submitter__description'})
        if not summary:
            return ''
        return normalize(summary.text)

    def instructions(self):
        """Return the instructions of the recipe."""
        instructions = self.soup.find(attrs={'class': 'recipe-directions__list'})
        if not instructions:
            raise RecipeParsingError("No instructions found")
        instruction_list = [x.text for x in instructions.findAll('span')]

        return instruction_list

    def image_url(self):
        """Return the url of the main recipe image."""
        photo_strip = self.soup.find(attrs={'class': 'photo-strip__items'})
        if not photo_strip:
            return ''
        li = photo_strip.find('li')
        if not li:
            return ''
        img_obj = li.find('img')
        if not img_obj:
            return ''
        img_src = img_obj['src']

        # img_src is thumbnail size. need to remove manual url scaping so it comes at native size.
        img_src = re.sub(r"/[0-9]+x[0-9]+/", "/", img_src)
        return img_src

    def time(self):
        """Return the total time to make in minutes."""
        time = self.soup.find(attrs={'class': 'ready-in-time'})
        if not time:
            return ''
        time_raw = time.text

        hour_match = re.search(r'([0-9]+) h', time_raw)
        minute_match = re.search(r'([0-9]+) m', time_raw)

        total_time = 0
        if hour_match:
            total_time += int(hour_match.group(1)) * 60
        if minute_match:
            total_time += int(minute_match.group(1))

        return str(total_time)

    def ingredients(self):
        """Return the ingredients, amounts, and units needed to make the recipe."""
        ingredients_raw = self.soup.find_all(attrs={'class': 'recipe-ingred_txt', 'itemprop': 'ingredients'})
        ingredients_raw_text = [item.text for item in ingredients_raw]

        UNITS = ['teaspoon', 'teaspoons', 'tsp', 't', 'tablespoon', 'tablespoons', 'tbsp', 'T',
            'pinch', 'pinches', 'shakes', 'dash', 'ounce', 'ounces', 'oz', 'pound', 'pounds', 'lb', 'lbs',
            'cup', 'cups', 'pint', 'pints', 'quart', 'quarts', 'gallon', 'gallons',
            'stalk', 'stalks', 'clove', 'cloves', 'packet', 'packets', 'can', 'cans', 'bunch', 'bunches',
            'loaf', 'loaves', 'package', 'packages', 'jar', 'jars', 'drop', 'drops']

        PARTIAL_INGREDIENT = ['skinless']

        ingredient_objs = []
        # Regular expression for extracting the unit
        reg_unit = re.compile(r'([0-9]*( ?[0-9]+/[0-9]+)?)? *(?P<unit>\w+)')
        # Regular expression for after the unit has been removed (ignores things after commas)
        reg = re.compile(r'^(?P<amount>[0-9]*( ?[0-9]+/[0-9]+)?)? *(\(.+\))? *(?P<ingredient>[\w \-\'®™]+)')
        # Regular expression for after the unit has been removed (takes entire line)
        reg_full = re.compile(r'^(?P<amount>[0-9]*( ?[0-9]+/[0-9]+)?)? *(\(.+\))? *(?P<ingredient>.+)')
        for item in ingredients_raw_text:
            raw_item = item
            unit_match = reg_unit.match(item)
            unit = ''
            # Try to match the unit and remove it
            if unit_match:
                m_unit = unit_match.group('unit')
                if m_unit and m_unit in UNITS:
                    unit = m_unit
                    item = re.sub(unit, '', item)

            # Then match the rest
            match = reg.match(item)
            if not match:
                raise IngredientParsingError(raw_item)

            amount = match.group('amount')
            ingredient = match.group('ingredient')

            # Match full line if the ingredient probably has a comma in it (like skinless, boneless chicken)
            if ingredient in PARTIAL_INGREDIENT:
                match = reg_full.match(item)
                if not match:
                    raise IngredientParsingError(raw_item)

                ingredient = match.group('ingredient')

            if not amount:
                amount = ''
            if not ingredient or ingredient.isspace():
                raise IngredientParsingError(raw_item)

            ingredient_objs.append({'amount': normalize(amount), 'unit': normalize(unit), 'ingredient': normalize(ingredient)})

        return ingredient_objs

    def appliances(self):
        """Return the appliances needed to make the recipe."""
        APPLIANCES = ['oven', 'microwave', 'deep-fryer', 'mixer', 'blender', 'food processor']

        instr = ' '.join(self.instructions())
        appliances = []
        for appliance in APPLIANCES:
            if instr.find(appliance) != -1 and appliance not in appliances:
                appliances.append(appliance)

        return appliances

    def difficulty(self):
        """This makes a default difficulty for a recipe based off of the number of ingredients"""
        numIng = len(self.soup.find_all(attrs={'class': 'recipe-ingred_txt', 'itemprop': 'ingredients'}))
        if(numIng < 5):
            #if there are less than 5 ingredients, assume it's easy difficulty.
            return 'E'
        if(numIng < 10):
            #if there are 5-9 ingredients, assume it's medium difficulty.
            return 'M'
        #if there are 10 or more ingredients, assume it's hard difficulty.
        return 'D'
