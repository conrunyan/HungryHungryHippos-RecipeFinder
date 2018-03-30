"""Holds the models for the scraper."""

from django.db import models

class ScrapeResult(models.Model):
    """Holds the resulting status of scraping a url."""

    # The job that scraped this url
    job_id = models.IntegerField()
    # The date and time when we scraped this url
    scrape_time = models.DateTimeField(auto_now_add=True)
    # The url from which we scraped this recipe
    source_url = models.CharField(max_length=200)
    # Whether the scrape was successful
    successful = models.BooleanField()
    # The type of error that occured
    error_type = models.CharField(max_length=50, null=True, blank=True)
    # An error if there was one
    error = models.CharField(max_length=300, null=True, blank=True)
    # Stack trace of error
    error_trace = models.TextField(null=True, blank=True)

    def __str__(self):
        """Display important information to the result."""
        return "{0} : {1}".format(self.successful, self.get_short_error())

    def get_short_error(self):
        """Return a short version of the error."""
        if self.error:
            return self.error[:50]
        return self.error
