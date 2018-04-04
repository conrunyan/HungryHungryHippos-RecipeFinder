"""Holds the routing information for the recipe app."""

from django.conf.urls import url

from . import views

app_name = "recipe"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_private_recipe', views.add_private_recipe, name='add_private_recipe'),
    url(r'^edit_private_recipe/(?P<id>[0-9]+)/', views.edit_private_recipe, name='edit_private_recipe'),
    url(r'^delete_recipe/(?P<id>[0-9]+)/', views.delete_recipe_view, name='delete_recipe_view'),
    url(r'^recipe_full_view/(?P<id>[0-9]+)/', views.recipe_full_view, name='recipe_full_view'),
    url(r'^get_recipes/$', views.get_recipes, name='get_recipes'),
]
