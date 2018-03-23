"""Tests the recipe backend and client."""

from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from django.test import Client

from .models import Recipe, Ingredient, RecipeIngredient, Group, Appliance

class RecipeModelTest(TestCase):
    """Tests the recipe model and methods."""

    def test_get_ingredients_with_no_ingredients(self):
        """Get ingredients of recipe with no associated ingredients."""
        # Populate database with ingredients that are not in the recipe.
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")
        ing3 = Ingredient.objects.create(group=group, name="Ing 3")
        # Create fake recipe to populate RecipeIngredient table.
        recipe_fake = Recipe.objects.create(title="Fake", instructions="fake")
        r1 = RecipeIngredient(recipe=recipe_fake, ingredient=ing1, amount=1)
        r2 = RecipeIngredient(recipe=recipe_fake, ingredient=ing2, amount=3)
        r1.save()
        r2.save()
        # Create real recipe to test against.
        recipe = Recipe.objects.create(title="Recipe", instructions="real")

        self.assertQuerysetEqual(recipe.get_ingredients(), [], "Empty recipe returns ingredients.")

    def test_get_ingredients_from_recipe(self):
        """Get ingredients of recipe that has ingredients."""
        # Populate database with ingredients that are not in the recipe.
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")
        ing3 = Ingredient.objects.create(group=group, name="Ing 3")
        # Create fake recipe to populate RecipeIngredient table.
        recipe_fake = Recipe.objects.create(title="Fake", instructions="fake")
        r1 = RecipeIngredient(recipe=recipe_fake, ingredient=ing1, amount=1)
        r2 = RecipeIngredient(recipe=recipe_fake, ingredient=ing2, amount=3)
        r1.save()
        r2.save()
        # Create real recipe to test against.
        recipe = Recipe.objects.create(title="Recipe", instructions="real")
        r3 = RecipeIngredient(recipe=recipe, ingredient=ing1, amount=3)
        r4 = RecipeIngredient(recipe=recipe, ingredient=ing3, amount=1)
        r3.save()
        r4.save()

        self.assertEquals(list(recipe.get_ingredients()), [ing1, ing3])

    def test_creating_ingredients_with_same_name_throws_error(self):
        """Assert error is thrown if two ingredients with the same name are created."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        self.assertRaises(IntegrityError, Ingredient.objects.create, group=group, name="Ing 1")

    def test_creating_group_with_same_name_throws_error(self):
        """Assert error is thrown if two ingredients with the same name are created."""
        group = Group.objects.create(name="Group 1")
        self.assertRaises(IntegrityError, Group.objects.create, name="Group 1")

    def test_get_appliances_with_no_appliances(self):
        """Get appliances of recipe with no associated appliances."""
        # Populate appliance table
        a1 = Appliance.objects.create(name="A 1")
        a2 = Appliance.objects.create(name="A 2")
        a1.save()
        a2.save()
        # Create empty recipe to test against
        recipe = Recipe.objects.create(title="Empty", instructions="Empty")

        self.assertEquals(list(recipe.get_appliances()), [], "Empty recipe returns appliances.")

    def test_get_appliances_from_recipe(self):
        """Get appliances of recipe with no associated appliances."""
        # Populate appliance table
        a1 = Appliance.objects.create(name="Appliance 1")
        a2 = Appliance.objects.create(name="Appliance 2")
        a3 = Appliance.objects.create(name="Appliance 3")
        a1.save()
        a2.save()
        a3.save()
        # Create empty recipe to test against
        recipe = Recipe.objects.create(title="Recipe", instructions="Empty")
        recipe.appliances.add(a1, a3)

        self.assertEquals(list(recipe.get_appliances()), [a1, a3])

    def test_default_visibility_is_private(self):
        """Check visibility of recipe is private by default."""
        recipe = Recipe.objects.create(title="Recipe", instructions="Empty")

        self.assertTrue(recipe.is_private)

    def test_can_create_valid_source_url(self):
        """Check creation of valid source url."""
        SOURCE_URL = "https://goodrecipes.com/recipes/awesome.html"
        recipe = Recipe.objects.create(title="Recipe", instructions="Empty", source_url=SOURCE_URL)

        self.assertEquals(recipe.source_url, SOURCE_URL)

    def test_can_create_blank_source_url(self):
        """Check creation of blank source url."""
        recipe = Recipe.objects.create(title="Recipe", instructions="Empty", source_url="")

        self.assertEquals(recipe.source_url, "")

    def test_can_create_null_source_url(self):
        """Check creation of null source url."""
        recipe = Recipe.objects.create(title="Recipe", instructions="Empty", source_url=None)

        self.assertIsNone(recipe.source_url)


class RecipeIngredientModelTest(TestCase):
    """Tests the RecipeIngredient model and methods."""

    def test_str_returns_string(self):
        """Test that the string of RecipeIngrient doesn't crash. Created for #6."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        recipe_fake = Recipe.objects.create(title="Fake", instructions="fake")
        r1 = RecipeIngredient(recipe=recipe_fake, ingredient=ing1, amount='1/2', unit='cup')

        self.assertIs(type(str(r1)), str)


class RecipeAppIndexTest(TestCase):
    """Test the recipe app index page."""

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_response_status_ok(self):
        """Check if the server response is 200."""
        response = self.client.get(reverse('recipe:index'))

        self.assertEquals(response.status_code, 200)

    def test_populates_ingredients(self):
        """Check if the server populates the ingredients from the database."""
        group1 = Group.objects.create(name="Group1")
        ing1_1 = Ingredient.objects.create(group=group1, name="Ing 1 1")
        ing1_2 = Ingredient.objects.create(group=group1, name="Ing 1 2")
        ing1_3 = Ingredient.objects.create(group=group1, name="Ing 1 3")
        group2 = Group.objects.create(name="Group2")
        group3 = Group.objects.create(name="Group3")
        ing3_1 = Ingredient.objects.create(group=group3, name="Ing 3 1")
        ing3_2 = Ingredient.objects.create(group=group3, name="Ing 3 2")

        response = self.client.get(reverse('recipe:index'))

        groups = response.context['groups']
        self.assertTrue(groups.exists())

        self.assertEquals(groups.count(), 3)
        self.assertEquals(groups.get(name='Group1'), group1)
        self.assertEquals(groups.get(name='Group2'), group2)
        self.assertEquals(groups.get(name='Group3'), group3)

        ingredient_set_1 = groups.get(name='Group1').ingredient_set.all()
        self.assertEquals(ingredient_set_1.count(), 3)
        self.assertEquals(ingredient_set_1.get(name='Ing 1 1'), ing1_1)
        self.assertEquals(ingredient_set_1.get(name='Ing 1 2'), ing1_2)
        self.assertEquals(ingredient_set_1.get(name='Ing 1 3'), ing1_3)

        ingredient_set_2 = groups.get(name='Group2').ingredient_set.all()
        self.assertEquals(ingredient_set_2.count(), 0)

        ingredient_set_3 = groups.get(name='Group3').ingredient_set.all()
        self.assertEquals(ingredient_set_3.count(), 2)
        self.assertEquals(ingredient_set_3.get(name='Ing 3 1'), ing3_1)
        self.assertEquals(ingredient_set_3.get(name='Ing 3 2'), ing3_2)
