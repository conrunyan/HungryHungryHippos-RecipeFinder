"""Holds the routing information for the recipe app."""

from django.conf.urls import url

from . import views

app_name = "recipe"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_private_recipe', views.add_private_recipe, name='add_private_recipe')
]
