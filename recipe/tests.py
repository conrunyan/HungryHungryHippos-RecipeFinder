"""Tests the recipe backend and client."""

import json

from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from django.test import Client
from accounts.models import PersistentIngredient
from django.contrib.auth.models import User

from .models import Recipe, Ingredient, RecipeIngredient, Group, Appliance, IngredientUtils, UserRating, Comment, Favorite
from .forms import CommentForm, RecipeForm, RecipeIngredientForm

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

class IngredientSearchTest(TestCase):
    """Test Searching of Recipes by Ingredient."""

    def setUp(self):
        """Get ingredients objects."""
        self.client = Client()

    def test_ingr_qs_intserection(self):
        """Tests the interesection of two ingredients."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")
        ing3 = Ingredient.objects.create(group=group, name="Ing 3")
        # Create fake recipe to populate RecipeIngredient table.
        recipe_one = Recipe.objects.create(title="Fake", instructions="fake")
        r1 = RecipeIngredient(recipe=recipe_one, ingredient=ing1, amount=1)
        r2 = RecipeIngredient(recipe=recipe_one, ingredient=ing2, amount=3)
        r1.save()
        r2.save()
        # Create real recipe to test against.
        recipe_two = Recipe.objects.create(title="Recipe", instructions="real")
        r3 = RecipeIngredient(recipe=recipe_two, ingredient=ing1, amount=3)
        r3.save()
        # Create real recipe3 to test against.
        recipe_three = Recipe.objects.create(title="Recipe2", instructions="real")
        r4 = RecipeIngredient(recipe=recipe_three, ingredient=ing1, amount=3)
        r5 = RecipeIngredient(recipe=recipe_three, ingredient=ing2, amount=1)
        r6 = RecipeIngredient(recipe=recipe_three, ingredient=ing3, amount=3)
        r4.save()
        r5.save()
        r6.save()

        expected_size = 1
        ing_utils = IngredientUtils()

        # save ingredient QS's in a list
        ing1 = ing1.recipe_set.values()
        ing2 = ing2.recipe_set.values()
        ing3 = ing3.recipe_set.values()
        ings = [ing1, ing2, ing3]
        # intersect QS's
        qs = ing_utils._ingredient_intersect(ings)
        # check number of recipes in the qs with minimum size of
        # base ingredient QuerySets
        self.assertEquals(len(qs), expected_size)

    def test_make_qs_list(self):

        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")
        ing3 = Ingredient.objects.create(group=group, name="Ing 3")
        # Create fake recipe to populate RecipeIngredient table.
        recipe_one = Recipe.objects.create(title="Fake", instructions="fake")
        r1 = RecipeIngredient(recipe=recipe_one, ingredient=ing1, amount=1)
        r2 = RecipeIngredient(recipe=recipe_one, ingredient=ing2, amount=3)
        r1.save()
        r2.save()
        # Create real recipe to test against.
        recipe_two = Recipe.objects.create(title="Recipe", instructions="real")
        r3 = RecipeIngredient(recipe=recipe_two, ingredient=ing1, amount=3)
        r3.save()
        # Create real recipe3 to test against.
        recipe_three = Recipe.objects.create(title="Recipe2", instructions="real")
        r4 = RecipeIngredient(recipe=recipe_three, ingredient=ing1, amount=3)
        r5 = RecipeIngredient(recipe=recipe_three, ingredient=ing2, amount=1)
        r6 = RecipeIngredient(recipe=recipe_three, ingredient=ing3, amount=3)
        r4.save()
        r5.save()
        r6.save()

        ing_utils = IngredientUtils()

        inglst = ["Ing 1", "Ing 2", "Ing 3"]
        qlst = ing_utils._make_qs_list(inglst)
        self.assertEqual(len(qlst), 3)

    def test_get_recipe_range(self):
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")
        ing3 = Ingredient.objects.create(group=group, name="Ing 3")
        # Create fake recipe to populate RecipeIngredient table.
        recipe_one = Recipe.objects.create(title="Fake", instructions="fake", is_private=False)
        r1 = RecipeIngredient(recipe=recipe_one, ingredient=ing1, amount=1)
        r2 = RecipeIngredient(recipe=recipe_one, ingredient=ing2, amount=3)
        r1.save()
        r2.save()
        # Create real recipe to test against.
        recipe_two = Recipe.objects.create(title="Recipe", instructions="real", is_private=False)
        r3 = RecipeIngredient(recipe=recipe_two, ingredient=ing1, amount=3)
        r3.save()
        # Create real recipe3 to test against.
        recipe_three = Recipe.objects.create(title="Recipe2", instructions="real", is_private=False)
        r4 = RecipeIngredient(recipe=recipe_three, ingredient=ing1, amount=3)
        r5 = RecipeIngredient(recipe=recipe_three, ingredient=ing2, amount=1)
        r6 = RecipeIngredient(recipe=recipe_three, ingredient=ing3, amount=3)
        r4.save()
        r5.save()
        r6.save()
        ing_utils = IngredientUtils()

        # make recipe list
        inglst = ["Ing 1", "Ing 2"]
        ing_qs = ing_utils._make_qs_list(inglst)
        recs = ing_utils._ingredient_intersect(ing_qs)

        # get recipe slice
        sliced_recs = ing_utils._get_recipe_range(recs, 0, 2)

        self.assertEquals(len(sliced_recs), 2)

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

class SearchRecipesBySelectedIngredientsTest(TestCase):
    """Test the return of the search algorithm for specified ingredients."""

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_get_recipes_view_returns_json_response_of_recipes(self):
        """Check if the search algorithm returns valid recipes based on the ingredients searched."""
        # create ingredients
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")
        ing3 = Ingredient.objects.create(group=group, name="Ing 3")
        # create a recipe with two ingredients
        recipe_one = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")
        r1 = RecipeIngredient(recipe=recipe_one, ingredient=ing1, amount=1)
        r2 = RecipeIngredient(recipe=recipe_one, ingredient=ing2, amount=3)
        r1.save()
        r2.save()
        # create another recipe with the third ingredient
        recipe_two = Recipe.objects.create(title="Recipe2", instructions="recipe2 instructions")
        r3 = RecipeIngredient(recipe=recipe_two, ingredient=ing3, amount=3)
        r3.save()

        response = self.client.post(reverse('recipe:get_recipes'), data='["Ing 1"]', content_type="application/json; charset=utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(str(response.content).find("Recipe1"), -1)
        self.assertEqual(str(response.content).find("Recipe2"), -1)

class PersistentIngredients(TestCase):
    """Tests the saving and loading of persistent ingredients for a user."""

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_anonymous_user_doesnt_save(self):
        """Test that an anonymous user doesn't save any ingredients (or crash the sever)."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")

        response = self.client.post(reverse('recipe:get_recipes'), data='["Ing 1","Ing 2"]', content_type="application/json; charset=utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(PersistentIngredient.objects.all())

    def test_adds_new_checked_ingredients(self):
        """Test that checking new ingredients saves them to be persistent."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")

        user = User.objects.create_user('test')
        self.client.force_login(user)
        response = self.client.post(reverse('recipe:get_recipes'), data='["Ing 1","Ing 2"]', content_type="application/json; charset=utf-8")

        self.assertEqual(response.status_code, 200)

        saved = PersistentIngredient.objects.filter(user=user)
        self.assertEqual(saved.count(), 2)
        self.assertTrue(saved.filter(ingredient=ing1))
        self.assertTrue(saved.filter(ingredient=ing2))

    def test_removes_unchecked_ingredients(self):
        """Test that unchecking ingredients removes them to be persistent."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")

        user = User.objects.create_user('test')
        self.client.force_login(user)

        pers1 = PersistentIngredient.objects.create(user=user, ingredient=ing1)
        pers2 = PersistentIngredient.objects.create(user=user, ingredient=ing2)

        response = self.client.post(reverse('recipe:get_recipes'), data='["Ing 2"]', content_type="application/json; charset=utf-8")

        self.assertEqual(response.status_code, 200)

        saved = PersistentIngredient.objects.filter(user=user)
        self.assertEqual(saved.count(), 1)
        self.assertTrue(saved.filter(ingredient=ing2))

    def test_multiple_users_with_same_ingredient(self):
        """#20: Check multiple users with same persistent ingredient."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")

        user1 = User.objects.create_user('test1')
        user2 = User.objects.create_user('test2')

        pers1 = PersistentIngredient.objects.create(user=user1, ingredient=ing1)
        pers2 = PersistentIngredient.objects.create(user=user2, ingredient=ing1)

        self.client.force_login(user1)

        response = self.client.post(reverse('recipe:get_recipes'), data='[]', content_type="application/json; charset=utf-8")

        self.assertEqual(response.status_code, 200)

        saved1 = PersistentIngredient.objects.filter(user=user1)
        self.assertEqual(saved1.count(), 0)

        saved2 = PersistentIngredient.objects.filter(user=user2)
        self.assertEqual(saved2.count(), 1)

    def test_anonymous_user_saves_in_session(self):
        """#22: Test that the anonymous user's ingredients are saved in the current session."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")

        self.client.post(reverse('recipe:get_recipes'), data='["Ing 1","Ing 2"]', content_type="application/json; charset=utf-8")

        persistent_ingredients = self.client.session['persistent_ingredients']
        self.assertTrue(persistent_ingredients)
        self.assertEquals(len(persistent_ingredients), 2)
        self.assertIn("Ing 1", persistent_ingredients)
        self.assertIn("Ing 2", persistent_ingredients)

    def test_anonymous_user_loads_from_session(self):
        """#22: Test that the anonymous user's ingredients are loaded from the current session."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        ing2 = Ingredient.objects.create(group=group, name="Ing 2")

        self.client.post(reverse('recipe:get_recipes'), data='["Ing 1","Ing 2"]', content_type="application/json; charset=utf-8")
        response = self.client.get(reverse('recipe:index'))

        persistent_ingredients = response.context['persistent_ingredients']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(persistent_ingredients)
        self.assertEquals(len(persistent_ingredients), 2)
        self.assertIn("Ing 1", persistent_ingredients)
        self.assertIn("Ing 2", persistent_ingredients)

class ViewingPrivateRecipes(TestCase):
    """Test viewing recipes that are marked is_private."""

    def setUp(self):
        """Setup the test client before each test."""
        self.client = Client()

    def test_returning_list_of_users_private_recipes(self):
        """Test that when a user navigates to 'My Recipes', they see all of their own recipes."""
        user1 = User.objects.create_user('test1')
        self.client.force_login(user1)
        user2 = User.objects.create_user('test2')
        # create a recipe with two ingredients
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        recipe_one = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions", user=user1)
        r1 = RecipeIngredient(recipe=recipe_one, ingredient=ing1, amount=1)
        r1.save()
        recipe_two = Recipe.objects.create(title="Recipe2", instructions="recipe2 instructions", user=user1)
        r2 = RecipeIngredient(recipe=recipe_two, ingredient=ing1, amount=2)
        r2.save()
        # make sure the view returns those two recipes and only those two
        response = self.client.get(reverse('myRecipes'))
        test = response.context['my_recipes']
        self.assertTrue(len(test) == 2)

    def test_viewing_private_recipe_for_same_user(self):
        """Test that a user can view their own recipe."""
        user1 = User.objects.create_user('test1')
        self.client.force_login(user1)
        # create a recipe with two ingredients
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        recipe_one = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions", user=user1)
        r1 = RecipeIngredient(recipe=recipe_one, ingredient=ing1, amount=1)
        r1.save()
        recipe_two = Recipe.objects.create(title="Recipe2", instructions="recipe2 instructions")
        r2 = RecipeIngredient(recipe=recipe_two, ingredient=ing1, amount=2)
        r2.save()

        response = self.client.get(reverse('recipe:recipe_full_view', kwargs={'id':recipe_one.id}))
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('recipe:recipe_full_view', kwargs={'id':recipe_two.id}))
        self.assertEqual(response2.status_code, 403)

    def test_guest_cannot_view_private_recipe(self):
        """Test that a guest cannot view private recipes."""
        group = Group.objects.create(name="TestGroup")
        ing1 = Ingredient.objects.create(group=group, name="Ing 1")
        recipe_one = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")
        r1 = RecipeIngredient(recipe=recipe_one, ingredient=ing1, amount=1)
        r1.save()

        response = self.client.get(reverse('recipe:recipe_full_view', kwargs={'id':recipe_one.id}))
        self.assertEqual(response.status_code, 403)

class FavoritesPage(TestCase):
    """Tests that the favorites page doesn't fail."""

    def setUp(self):
        """Create client to make requests."""
        self.client = Client()

    def test_guest_cannot_access_page(self):
        """Test that a user cannot acccess the Favorites page if they are not logged in."""
        user1 = User.objects.create_user('test1')
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)

    def test_no_favorited_recipes(self):
        """Test the favorites page when there are no favorited recipes."""
        user1 = User.objects.create_user('test1')
        self.client.force_login(user1)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)

    def test_some_favorited_recipes(self):
        """Test that the Favorites page displays the correct number of recipes."""
        user1 = User.objects.create_user('test1')
        self.client.force_login(user1)
        recipe1 = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")
        recipe2 = Recipe.objects.create(title="Recipe2", instructions="recipe2 instructions")
        fav1 = Favorite.objects.create(recipe=recipe1, user=user1)
        fav2 = Favorite.objects.create(recipe=recipe2, user=user1)
        response = self.client.get(reverse('favorites'))
        self.assertIs(response.context['favorites'].count(), 2)

class RecipeRating(TestCase):
    """Tests rating recipes for the user."""

    def setUp(self):
        """Create client to make requests."""
        self.client = Client()

    def test_no_ratings_is_none(self):
        """Test that a recipe with no ratings has a rating of None."""
        recipe = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")

        self.assertIsNone(recipe.get_rating())

    def test_rating_is_an_average(self):
        """Test that a recipe rating is the average ratings."""
        recipe = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")
        user = User.objects.create_user('test_user')
        user2 = User.objects.create_user('test_user2')
        UserRating.objects.create(recipe=recipe, user=user, value=4.1)
        UserRating.objects.create(recipe=recipe, user=user2, value=1.8)

        self.assertAlmostEqual(recipe.get_rating(), 2.95)

    def test_rating_count_zero(self):
        """Test that a recipe with no ratings has a rating count of 0."""
        recipe = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")

        self.assertEqual(recipe.get_rating_count(), 0)

    def test_rating_count(self):
        """Test that a recipe rating counts ratings."""
        recipe = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")
        user = User.objects.create_user('test_user')
        user2 = User.objects.create_user('test_user2')
        UserRating.objects.create(recipe=recipe, user=user, value=4.1)
        UserRating.objects.create(recipe=recipe, user=user2, value=1.8)

        self.assertEqual(recipe.get_rating_count(), 2)

    def test_adds_new_rating(self):
        """Test that a user can submit a new rating."""
        recipe = Recipe.objects.create(title="Recipe1", instructions="recipe1 instructions")
        user = User.objects.create_user('test_user')
        self.client.force_login(user)

        response = self.client.post(reverse('recipe:rate', kwargs={'id':recipe.id}),
            data='{"rating":"3"}', content_type="application/json; charset=utf-8")

        self.assertEquals(response.status_code, 200)

        result = response.json()

        self.assertEquals(result['valid'], 'True')
        self.assertEquals(result['average'], 3)
        self.assertEquals(result['count'], 1)

class TestCommentForm(TestCase):
    """Tests the comment form"""

    def test_init(self):
        commentForm = CommentForm(data={'content': "This is a comment!"})
        self.assertTrue(commentForm.is_valid())

    def test_init_without_content(self):
        commentForm = CommentForm(data={})
        self.assertFalse(commentForm.is_valid())

class TestFullViewAddComment(TestCase):

    def setUp(self):
        """Create client to make requests."""
        self.user = User.objects.create_user("test_user")
        self.content = "This is a comment!"
        self.client = Client()
        self.recipe = Recipe.objects.create(title="Recipe", instructions="real", user=self.user, is_private=False)
        self.private_recipe = Recipe.objects.create(title="Recipe", instructions="real", user=self.user)

    def test_successful_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('recipe:recipe_full_view', kwargs={'id':self.recipe.id}), data={'content':self.content})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(recipe=self.recipe).user, self.user)
        self.assertEqual(Comment.objects.get(recipe=self.recipe).content, self.content)
        self.assertEqual(Comment.objects.get(recipe=self.recipe).recipe, self.recipe)

    def test_user_not_logged_in(self):
        response = self.client.get(reverse('recipe:recipe_full_view', kwargs={'id':self.recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please log in to post a comment.")

        response = self.client.post(reverse('recipe:recipe_full_view', kwargs={'id':self.recipe.id}), data={'content':self.content})
        self.assertEqual(response.status_code, 403)

    def test_no_context(self):
        self.client.force_login(self.user)
        comment_form = CommentForm(data={'content':self.content})
        response = self.client.post(reverse('recipe:recipe_full_view', kwargs={'id':self.recipe.id}), data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.all().exists())

    def test_private_recipe_with_same_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('recipe:recipe_full_view', kwargs={'id':self.recipe.id}), data={'content':self.content})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(recipe=self.recipe).user, self.user)
        self.assertEqual(Comment.objects.get(recipe=self.recipe).content, self.content)
        self.assertEqual(Comment.objects.get(recipe=self.recipe).recipe, self.recipe)

    def test_private_recipe_with_different_user(self):
        self.client.force_login(User.objects.create_user('hacker_man'))
        response = self.client.post(reverse('recipe:recipe_full_view', kwargs={'id':self.private_recipe.id}), data={'content':self.content})
        self.assertFalse(Comment.objects.all().exists())
        self.assertEqual(response.status_code, 403)

class TestRecipeForm(TestCase):
    """Tests the add Recipe Form."""

    def test_init_easy_difficulty(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'difficulty': "E",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertTrue(recipeForm.is_valid())

    def test_init_medium_difficulty(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'difficulty': "M",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertTrue(recipeForm.is_valid())

    def test_init_hard_difficulty(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'difficulty': "D",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertTrue(recipeForm.is_valid())

    def test_init_invalid_difficulty(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'difficulty': "Z",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertFalse(recipeForm.is_valid())

    def test_init_without_title(self):
        recipeForm = RecipeForm(data={'summary': "It's delicious!",
                                      'difficulty': "E",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertFalse(recipeForm.is_valid())

    def test_init_without_summary(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'difficulty': "E",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertFalse(recipeForm.is_valid())

    def test_init_without_difficulty(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertFalse(recipeForm.is_valid())

    def test_init_without_time(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'difficulty': "E",
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg",
                                      'instructions': "Make all of the things!"})
        self.assertFalse(recipeForm.is_valid())

    def test_init_without_image_url(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'difficulty': "E",
                                      'time': 10,
                                      'instructions': "Make all of the things!"})
        self.assertFalse(recipeForm.is_valid())

    def test_init_without_instructions(self):
        recipeForm = RecipeForm(data={'title': "A Recipe",
                                      'summary': "It's delicious!",
                                      'difficulty': "E",
                                      'time': 10,
                                      'image_url': "https://images.media-allrecipes.com/userphotos/600x600/439002.jpg"})
        self.assertFalse(recipeForm.is_valid())

class TestRecipeIngredientForm(TestCase):
    """Tests the add Recipe Form."""

    def setUp(self):
        group = Group.objects.create(name="TestGroup")
        self.ingredient = Ingredient.objects.create(group=group, name="Ing 1")

    def test_init(self):
        recipeIngredientForm = RecipeIngredientForm(data={'ingredient': 1, 'amount': '3', 'unit': 'cups'})
        self.assertTrue(recipeIngredientForm.is_valid())

    def test_init_without_unit(self):
        recipeIngredientForm = RecipeIngredientForm(data={'ingredient': 1, 'amount': '3'})
        self.assertTrue(recipeIngredientForm.is_valid())

    def test_init_without_amount(self):
        recipeIngredientForm = RecipeIngredientForm(data={'ingredient': 1, 'unit': 'cups'})
        self.assertTrue(recipeIngredientForm.is_valid())

    def test_init_without_amount_or_unit(self):
        recipeIngredientForm = RecipeIngredientForm(data={'ingredient': 1})
        self.assertTrue(recipeIngredientForm.is_valid())

    def test_init_without_ingredient(self):
        recipeIngredientForm = RecipeIngredientForm(data={'amount': '3', 'unit': 'cups'})
        self.assertFalse(recipeIngredientForm.is_valid())
