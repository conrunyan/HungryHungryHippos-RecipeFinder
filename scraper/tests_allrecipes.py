"""Tests the allrecipes scraper."""

import os
from django.test import TestCase
from .allrecipes import AllRecipes

class TestAllRecipes(TestCase):
    """Tests the allrecipes scraper."""

    def setUp(self):
        """Load the test html into the scraper."""
        with open(os.path.join(
            # Run from manage.py directory
            os.getcwd(),
            'scraper',
            'test_html',
            'allrecipes.html'
        )) as html:
            self.scraper = AllRecipes(html, test=True)

    def test_host_name(self):
        """Test the host name."""
        self.assertEqual('www.allrecipes.com', self.scraper.host_name())

    def test_title(self):
        """Test the title of the recipe."""
        self.assertEqual('Easy Garlic Broiled Chicken', self.scraper.title())

    def test_summary(self):
        """Test the summary of the recipe."""
        SUMMARY = "\"This very easy dish works with any cut of chicken, skin on or off...even with whole split chickens. My family loves this and it takes no time at all. Don't omit the parsley.\""

        self.assertEqual(SUMMARY, self.scraper.summary())

    def test_instructions(self):
        """Test the instructions of the recipe."""
        INSTRUCTIONS = ["Preheat the oven broiler. Lightly grease a baking pan.",
            "In a microwave safe bowl, mix the butter, garlic, soy sauce, pepper, and parsley. Cook 2 minutes on High in the microwave, or until butter is melted.",
            "Arrange chicken on the baking pan, and coat with the butter mixture, reserving some of the mixture for basting.",
            "Broil chicken 20 minutes in the preheated oven, until juices run clear, turning occasionally and basting with remaining butter mixture. Sprinkle with parsley to serve."]

        self.assertListEqual(INSTRUCTIONS, self.scraper.instructions())

    def test_image_url(self):
        """Test the url of the image after it is resized."""
        IMAGE_URL="https://images.media-allrecipes.com/userphotos/600x600/4486670.jpg"

        self.assertEqual(IMAGE_URL, self.scraper.image_url())

    def test_time(self):
        """Test the total time in minutes of the recipe."""
        self.assertEqual("30", self.scraper.time())

    def test_ingredients(self):
        """Test the ingredients of the recipe."""
        INGREDIENTS = ['butter', 'minced garlic', 'soy sauce', 'black pepper',
            'dried parsley', 'boneless chicken thighs', 'dried parsley']

        scraper_ingredients = [x['ingredient'] for x in self.scraper.ingredients()]

        self.assertListEqual(INGREDIENTS, scraper_ingredients)

    def test_units(self):
        """Test the units of the ingredients."""
        UNITS = ['cup', 'tablespoons', 'tablespoons', 'teaspoon', 'tablespoon', '', '']

        scraper_units = [x['unit'] for x in self.scraper.ingredients()]

        self.assertListEqual(UNITS, scraper_units)

    def test_amounts(self):
        """Test the amounts of the ingredients."""
        AMOUNTS = ['1/2', '3', '3', '1/4', '1', '6', '']

        scraper_amounts = [x['amount'] for x in self.scraper.ingredients()]

        self.assertListEqual(AMOUNTS, scraper_amounts)

    def test_appliances(self):
        """Test the appliances required for the recipe."""
        APPLIANCES = ['oven', 'microwave']

        self.assertListEqual(APPLIANCES, self.scraper.appliances())
