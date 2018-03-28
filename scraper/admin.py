"""Register models to be displayed in the admin view."""

from django.contrib import admin

from . import models

class ScrapeResultAdmin(admin.ModelAdmin):
    """Define display for ScrapeResult in admin app."""

    list_display = ('scrape_time', 'successful', 'source_url', 'error_type', 'error')
    model = models.ScrapeResult

admin.site.register(models.ScrapeResult, ScrapeResultAdmin)
