"""Holds the views for the index page."""

import json

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import PersistentIngredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet, CommentForm
from .ingredient_functions import save_ingredients_to_user, get_ingredient_objs_of_user, get_ingredient_names
from .models import Group, Recipe, RecipeIngredient, IngredientUtils, Ingredient, Comment, UserRating, Appliance, Favorite


def index(request):
    """Return the base index page for the site."""
    groups = Group.objects.order_by("name")
    group_dict = {}
    for group in groups:
        ing_list = list(group.ingredient_set.all().order_by("name"))
        group_dict[group.name] = ing_list

    ingredientsAreSelected = False
    ingredients = Ingredient.objects.order_by("name")

    persistent_ingredients = []
    if request.user:
        persistent_ingredients = get_ingredient_objs_of_user(request.user, request.session)
        persistent_ingredients = get_ingredient_names(persistent_ingredients)

    appliances = Appliance.objects.order_by("name")
    difficulties = ["Easy", "Medium", "Hard"]
    # time = ["0-30 min", "31-60 min", "1+ hr"]
    time = [30, 60, 120]

    context = {"groups": groups, "group_dict": group_dict, "ingredientsAreSelected": ingredientsAreSelected,
               "persistent_ingredients": persistent_ingredients, "ingredients_list": ingredients, "appliances": appliances, "difficulties": difficulties, "time": time}
    return HttpResponse(render(request, 'recipe/index.html', context))


@csrf_exempt
def get_recipes(request):
    """Get a JSON object of recipes from the search algorithm."""
    if not request.body:
        return JsonResponse({})

    # parse json string to list of ingredient names
    ing = request.body.decode("utf-8")
    ingredients_to_search_by = ing[1:-1].replace('"', "").split(',')
    # save ingredients for the future
    # get user id, if applicable. Else default to 0
    usr_id = 0
    if request.user:
        save_ingredients_to_user(request.user, ingredients_to_search_by, request.session)
        usr_id = request.user.id
    # send ingredients to search algorithm
    found_recipes = IngredientUtils(usr_id).find_recipes(ingredients_to_search_by)
    # convert queryset to JSON!!!
    values = list(found_recipes.values())

    for recipe in values:
        recipe['appliances'] = list(Appliance.objects.filter(recipe=recipe['id']).values('name'))

    return JsonResponse({'results': values})


def recipe_full_view(request, id):
    """Return the full view of a recipe."""
    current_recipe = get_object_or_404(Recipe, id=id)
    if current_recipe.is_private and current_recipe.user != request.user:
        raise PermissionDenied

    isFavorite = 0
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(recipe=current_recipe, user=request.user)
        if (favorites.count() != 0):
            isFavorite = 1

    if (request.method == 'POST' and request.user.is_authenticated()):
        comment_form = CommentForm(request.POST)
        comment = comment_form.save(commit=False)
        comment.recipe = current_recipe
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect('#')


    comment_form = '' #blank if not logged on
    comments = Comment.objects.filter(recipe=current_recipe).order_by('-creation_date')
    if request.user.is_authenticated():
        comment_form = CommentForm()
    ingredients = RecipeIngredient.objects.filter(recipe=current_recipe)
    context = {'current_recipe': current_recipe,
               'ingredients': ingredients,
               'comments': comments,
               'comment_form': comment_form,
               'isFavorite': isFavorite}

    return HttpResponse(render(request, 'recipe/recipe_full_view.html', context))


def rate(request, id):
    """Rate a recipe. Update previous rating if exists or create new rating.

    Return if updating the rating succeded.
    Return the updated rating for the recipe if everything goes swimmingly.
    """
    recipe = get_object_or_404(Recipe, id=id)
    rating = 0
    if request.user.is_authenticated:
        try:
            user_rating = UserRating.objects.get(recipe=recipe, user=request.user)
            rating = user_rating.value
        except UserRating.DoesNotExist:
            rating = None

    if request.method == 'GET':
        return JsonResponse({'valid': 'True',
                             'average': recipe.get_rating(),
                             'user_rating': rating,
                             'count': recipe.get_rating_count()})

    if not request.user.is_authenticated:
        raise PermissionDenied

    try:
        rating = json.loads(request.body.decode("utf-8"))['rating']
        rating = float(rating)
    except KeyError:
        return JsonResponse({'error': 'Rating not sent'})
    except ValueError as e:
        return JsonResponse({'error': str(e)})
    # clamp rating to valid values (1-5)
    rating = min(5.0, max(1.0, rating))

    UserRating.objects.update_or_create(recipe=recipe, user=request.user, defaults={'value': rating})

    return JsonResponse({'valid': 'True',
                         'average': recipe.get_rating(),
                         'user_rating': rating,
                         'count': recipe.get_rating_count()})

@login_required
def favorite(request, id):
    if request.body:
        body = request.body.decode("utf-8")
        isFavorite = json.loads(body)['isFavorite']
        recipe = get_object_or_404(Recipe, id=id)
        if (isFavorite == 0):
            faved = Favorite.objects.filter(recipe=recipe, user=request.user)
            faved.delete()
        else:
            fav = Favorite.objects.create(recipe=recipe, user=request.user)
    return redirect('recipe:recipe_full_view', id=id)

@login_required
def add_private_recipe(request):
    """Create a view with a form for adding a recipe."""
    if(request.method == 'POST'):
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            for ingredient_form in formset:
                if(ingredient_form.has_changed()):
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()
            return redirect('recipe:recipe_full_view', recipe.id)

    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    context = {'form': form,
               'formset': formset}
    return HttpResponse(render(request, 'recipe/add_private_recipe.html', context))

@login_required
def edit_private_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.user != request.user:
        raise PermissionDenied

    if(request.method == 'POST'):
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('recipe:recipe_full_view', id)

    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)


    context = {'form': form,
               'formset': formset,
               'recipe_id': recipe.id}
    return HttpResponse(render(request, 'recipe/edit_private_recipe.html', context))

def delete_recipe_view(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.user != request.user:
        raise PermissionDenied

    recipe.delete()
    return redirect('recipe:index')

def submit_for_public(request, id):
    """Submits recipe for migration to public, redirecting user to 'submission' screen"""

    recipe = get_object_or_404(Recipe, id=id)
    # check if recipe is owned by user
    if recipe.user == request.user:
        # if yes, check if recipe is already public
        if not recipe.is_private:
            return redirect('recipe:recipe_full_view', id)
        else:
            # TODO: Add submission to admin back-log here. For now, make the recipe public
            print('SUBMITTED')
            recipe.is_private = False
            recipe.save()
    # if not, redirect to recipe full_view
    else:
        return redirect('recipe:recipe_full_view', id)
    context = {'current_recipe': recipe.id,}
    return HttpResponse(render(request, 'recipe/submit_for_public.html', context))
