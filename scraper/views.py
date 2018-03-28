"""Holds the views for the scraper."""

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.html import escape
from django.contrib.admin.views.decorators import staff_member_required
from . import utils
from .job_processor import submit_job

@staff_member_required(login_url='login')
def scrape(request):
    """User interface for the scraper."""
    if request.method == 'GET':
        return render(request, 'scraper/create_job.html')

    # Assume post
    form_errors = []

    site_url = escape(request.POST.get('sample-url', ''))
    start = escape(request.POST.get('id-start', ''))
    count = escape(request.POST.get('id-count', ''))

    if not site_url:
        form_errors.append('Site url invalid or empty')
    if not start:
        form_errors.append('Start invalid or empty')
    if not count:
        form_errors.append('Count invalid or empty')

    end = 0
    if not form_errors:
        try:
            start = int(start)
            end = start + int(count)
        except Exception as e:
            form_errors.append(e)

    if form_errors:
        return render(request, 'scraper/create_job.html', {'errors': form_errors})

    job_errors = []
    job_id = -1
    try:
        job_id = submit_job(site_url, start, end, request.user)
    except Exception as e:
        job_errors.append('Job raised exception: {}'.format(e))

    context = {'job_id': job_id, 'errors': job_errors}
    return render(request, 'scraper/job_status.html', context)

@staff_member_required(login_url='login')
def scrape_batch(request, start, end):
    """Scrape and save a batch of recipes based on passed parameters."""
    start = int(start)
    end = int(end)
    if start > end:
        return HttpResponse('Start must be less than end')

    site_url = escape(request.GET.get('url', ''))

    try:
        submit_job(site_url, start, end, request.user)
    except Exception as e:
        return HttpResponse('Job threw unexpected error: {}'.format(e))

    return HttpResponse('Job submitted successfully')

@staff_member_required(login_url='login')
def scrape_and_display(request):
    """Return a json object from a given url. URL is specified by '?url=' parameter."""
    return JsonResponse(utils.scrape_to_json(escape(request.GET.get('url', ''))))

@staff_member_required(login_url='login')
def scrape_and_save(request):
    """Parse a url and save it to the database."""
    return HttpResponse(utils.scrape_and_save(escape(request.GET.get('url', '')), request.user))
