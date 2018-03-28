"""Register models to be displayed in the admin view."""

from django.contrib import admin

from . import models

class ScrapeResultAdmin(admin.ModelAdmin):
    """Define display for ScrapeResult in admin app."""

    list_display = ('job_id', 'scrape_time', 'successful', 'source_url', 'error_type', 'get_short_error')
    model = models.ScrapeResult

admin.site.register(models.ScrapeResult, ScrapeResultAdmin)
