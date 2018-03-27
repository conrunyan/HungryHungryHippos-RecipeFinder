"""Holds the urls for the scraper app. Already prefixed with 'scraper/'."""

from django.conf.urls import url

from . import views

app_name = "scraper"
urlpatterns = [
    url(r'^display/$', views.scrape_and_display, name='scrape_and_display'),
    url(r'^$', views.scrape_and_save, name='scrape_and_save')
]
