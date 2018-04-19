"""Holds the recipe models for the database."""

from django.db import models
from django.db.models import Q, QuerySet, Avg
from django.contrib.auth.models import User
from django.utils import timezone
from itertools import chain

class Group(models.Model):
    """This represents a food category.

    Each ingredient has a single category. In the web-app, the ingredients are
    categorized by these groups.
    """

    # The name of the group
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.name


class Ingredient(models.Model):
    """This is an ingredient to recipes.

    Each ingredient may be a part of many recipes and each recipe may have many
    ingredients. The purpose of this class is to provide consistent naming between
    ingredients and easier filtering of recipes by ingredient. Each recipe is a part
    of a group.
    """

    # The group which this ingredient belongs to
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # The name of this ingredient
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.name

    def get_recipes(self):
        """Return a QuerySet of associated Recipes."""
        return self.recipe_set.values()

    def get_recipe_ids(self):
        """Returns a list of associated Recipe IDs"""
        my_recs = list(self.get_recipes())
        # get just the ids from each record
        rec_ids = [rec['id'] for rec in my_recs]
        return rec_ids


class IngredientUtils():
    """Class of ingredient helper functions.

    Contains methods to help search for recipes by ingredient
    """
    def __init__(self, user_id=0):
        self.user_id = user_id

    def __str__(self):
        return "Ingredient Tools"

    def find_recipes(self, ingredients, start=0, end=200):
        """Returns a QuerySet of Recipes
        Given a list of ingredients and a range, the database
        will be queried to find all recipes with common association
        between the ingredients.

        Once these are found, the range provided will determine how
        many recipes are actually returned.
        """

        recipe_qs = self._make_qs_list(ingredients)
        recipe_list = self._dict_to_qs(recipe_qs)
        # if ingredients were found...
        if len(recipe_list) > 0:
            # slice recipe list
            recipe_list = recipe_list[start:end]
        # return empty queryset
        else:
            emp_qs = Recipe.objects.none()
            recipe_list = list(emp_qs.values())
            # print('Returning:', emp_qs)
        return recipe_list

    def _ingredient_intersect(self, ing_qs_list):
        """Returns a QuerySet of recipes shared between ingredients"""

        #return QuerySet.intersection(*ing_qs_list)
        return QuerySet.union(*ing_qs_list)

    def _filter_private_recs(self, recipe):
        """Returns public recipes and the user's private recipes (if applicable)"""
        #private_q = Q(is_private=False)
        #usr_id_q = Q(user_id=self.user_id)
        ## get public recipes or those that belong to the user
        if not recipe.is_private or recipe.user_id == self.user_id:
            return recipe
        else:
            return None

    def _make_qs_list(self, ingredients):
        """Returns a Dictionary of QuerySets of recipes given a list of ingredient names"

        Given a list of Ingredients, this function will search for recipes
        linked to each ingredient, then sorts them.
        Each recipe is sorted into a bucket based on how many ingredients it contains from the ing_list.
        Buckets are classified by a percentage of ingredients the recipes contain:
            -i.e. ['flour', 'sauce', 'cheese', 'water'] are passed as ingredients. Looking at the "Sausage Pizza" recipe, 
            all ingredients, except sausage, are passed in the ingredients list. This recipe would be placed in the 4/5 (80%) bucket
        """

        recipe_dict = {}
        used_recs = [] # list of rec ids that were actually used
        # loop over ingredients, finding recipes associated with
        # each ingredient, then sorting them by percent of ingredients
        for ing in ingredients:
            try:
                cur_ing = Ingredient.objects.get(name=ing)
                rec_ids = cur_ing.get_recipe_ids()
                cur_ing_recs = Recipe.objects.filter(id__in=(rec_ids))
            # if ingredient found, get recipes
                if len(cur_ing_recs) > 0:
                    # get recipe percentages
                    for rec in cur_ing_recs:
                        tmp_perc = rec.get_perc_ingredients(ingredients)
                        # filter recipe (skip if private and not the user's)
                        filtered_rec = self._filter_private_recs(rec)
                        if filtered_rec is not None:
                            # add to recipe percent buckets.
                            rec_to_save = list(Recipe.objects.filter(id=filtered_rec.id).values())
                            if tmp_perc in recipe_dict:
                                # remove duplicates
                                if rec_to_save not in recipe_dict[tmp_perc]:
                                    recipe_dict[tmp_perc].append(rec_to_save)
                            else:
                                recipe_dict[tmp_perc] = [rec_to_save]
            # else, ingredient does not exist in the database
            except (Ingredient.DoesNotExist):
               continue

        return recipe_dict

    def _get_recipe_range(self, recipe_list, start, end):
        """Returns a slice of a Recipe QuerySet

        NOTE: Currently set to sort by "title". Can be changed to
        whatever we want the recipes to be sorted by.
        """
        return recipe_list.order_by('title')[start:end]

    def _dict_to_qs(self, dict):
        """Converts dictionary of recipes into a sorted list"""
        keys = sorted(dict.keys())
        keys.sort(reverse=True)
        out_lst = []
        
        # for each list of QS's, append it to the out_lst of recipes
        # from greatest to least
        for key in keys:
            out_lst += dict[key]
        # Found this nifty tool on StackOverflow :)
        new_qs = list(chain(*out_lst))
        return new_qs



class Appliance(models.Model):
    """This is an appliance that is required to make a recipe.

    A recipe may
    have 0+ appliances. The purpose of this class is to provide consistent
    naming between appliances and easier filtering of recipes by appliance.
    """

    # The name of this appliance
    name = models.CharField(max_length=40)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.name


class Recipe(models.Model):
    """This holds all the attributes of a recipe.

    The title and summary display when the recipe is shown as a search result.
    The user is the user that submitted the recipe. The time is measured in minutes.
    The image_url points to either an internal or external image location. The
    rating ranges between zero and five. The ingredients and appliances have a
    many-to-many relationship with a recipe.
    """

    # Title of the recipe
    title = models.CharField(max_length=50)
    # Short summary of the recipe (to be used on preview when searching)
    summary = models.CharField(max_length=280, null=True, blank=True)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False)
    DIFFICULTY_CHOICES = (
        ('', '--Difficulty--'),
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('D', 'Hard')
    )
    # The actual difficulty of the recipe
    difficulty = models.CharField(max_length=1, null=True,
                                  choices=DIFFICULTY_CHOICES)
    # The time it takes to make the recipe (in minutes)
    time = models.IntegerField(null=True, blank=True)
    # The image url to be used to showcase the recipe (used in both search and
    # detailed views)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    # The detailed instructions to make the recipe
    instructions = models.TextField()
    # The date this recipe object was created
    creation_date = models.DateField(auto_now_add=True, editable=False)
    # The ingredient set of ingredients that is required for this recipe
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')
    # The appliance set of appliances needed for this recipe
    appliances = models.ManyToManyField(Appliance)
    # If the recipe is a user's private recipe
    is_private = models.BooleanField(default=True)
    # The url from which we scraped this recipe
    source_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return self.title

    def get_ingredients(self):
        """Return a queryset of the ingredients in this recipe."""
        return self.ingredients.all()

    def get_appliances(self):
        """Return a queryset of the appliances required by this recipe."""
        return self.appliances.all()

    def get_rating(self):
        """Return the average rating for the recipe."""
        return self.userrating_set.all().aggregate(Avg('value'))['value__avg']

    def get_rating_count(self):
        """Return the number of ratings for the recipe."""
        return self.userrating_set.all().count()

    def get_perc_ingredients(self, usr_ingredients):
        """Returns a percentage (i.e. 80 for 80%) ingredients needed.

        Determines the percentage of needed ingredients (what the recipe calls for)
        based on the ingredients specified by the user.
        """

        INGR_NAME_POS = 2
        # convert recipe ingredients to a list of names
        pre_ingr_list = list(self.ingredients.values_list())
        ingr_list = [ing[INGR_NAME_POS] for ing in pre_ingr_list]
        
        # convert user ingredient list and recipe ingredient lists to sets, then perform
        # a bitwise AND on these sets (will only return the ingredients they share)
        cur_rec_ings = set(ingr_list)
        usr_rec_ings = set(usr_ingredients)
        shared_ings = cur_rec_ings & usr_rec_ings
        # get number of ingredients shared, and required by recipe
        num_shared = len(shared_ings)
        num_rec_ings = len(ingr_list)
        # return the ratio of number of ingredients passed to number of ingredients called for
        # NOTE: Truncates the decimals
        return int((num_shared/num_rec_ings) * 100)


class RecipeIngredient(models.Model):
    """This class is used in the relationship between recipes and ingredients.

    This class adds an amount of an ingredient as well as its unit.
    """

    # The Recipe that this RecipeIngredient connection refers to
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # The Ingredient that this RecipeIngredient connection refers to
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # The amount of this ingredient in the recipe
    amount = models.CharField(max_length=10, null=True, blank=True)
    # The unit which the amount is measured in
    unit = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return str(self.recipe)


class Comment(models.Model):
    """This holds a comment on a recipe."""

    # The Recipe that this comment refers to
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # The user that submitted this comment
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # The content of the comment
    content = models.CharField(max_length=500)
    # The time the comment was created
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a string to identify the object in the admin app."""
        return str(self.recipe)


class UserRating(models.Model):
    """Holds a rating given by a user to a recipe."""

    # Holds the recipe this rating is for
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # Holds the user that submitted this rating
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Holds the rating this user gave (ranges from 1.0 to 5.0)
    value = models.FloatField()

    def __str__(self):
        """Construct a string representation of this rating link."""
        return '{0} ({1}) : {2}'.format(self.recipe, self.user, self.value)
