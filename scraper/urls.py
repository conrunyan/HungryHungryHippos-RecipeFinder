"""Holds the urls for the scraper app. Already prefixed with 'scraper/'."""

from django.conf.urls import url

from . import views

app_name = "scraper"
urlpatterns = [
    url(r'^$', views.scrape, name='scrape'),
]
