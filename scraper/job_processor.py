"""Processes the jobs created by a batch request."""

from threading import Thread, Lock
from queue import Queue
import time
import traceback
from .scraper_functions import get_batch
from .utils import scrape_and_save
from .errors import UnknownWebsiteError, RecipeParsingError
from urllib.error import URLError
from random import randint
from .models import ScrapeResult

def submit_job(urls, begin, end, user):
    """Submit a job on a separate thread."""
    job_id = randint(10000000, 99999999)

    thread = WrapperThread(job_id, urls, begin, end, user)
    thread.daemon = True
    thread.start()

    return job_id

class WrapperThread(Thread):
    """Creates a job processor on a new thread."""

    def __init__(self, job_id, urls, begin, end, user):
        """Create a wrapper thread to start the job processor."""
        Thread.__init__(self)
        self.name = "WrapperThread-{}".format(job_id)
        self.urls = urls
        self.begin = begin
        self.end = end
        self.user = user
        self.job_id = job_id

    def run(self):
        """Create a JobProcessor on a new thread."""
        processor = JobProcessor(self.job_id, self.user, num_threads=4)
        processor.add_jobs(self.urls, self.begin, self.end)
        processor.wait()
        print("Done with job")

class JobProcessor():
    """Manages the processing of a set of jobs."""

    def __init__(self, job_id, user, num_threads=2):
        """Create a JobProcessor with the specified number of threads."""
        self.queue = Queue()
        self.queueLock = Lock()
        self.threads = []
        for i in range(1, num_threads + 1):
            self.threads.append(ScraperThread(job_id, self.queueLock, self.queue, user))

        for i in self.threads:
            i.start()

    def add_jobs(self, urls, begin, end):
        """Add the jobs to the processor and start executing them."""
        batch = get_batch(urls, begin, end)
        self.queueLock.acquire()
        for site in batch:
            self.queue.put(site)
        self.queueLock.release()

    def wait(self):
        """Block until the processor is finished running."""
        while not self.queue.empty():
            pass
        for thread in self.threads:
            thread.should_exit = True
        for thread in self.threads:
            thread.join()

class ScraperThread(Thread):
    """Continually prcesses jobs in a queue."""

    def __init__(self, job_id, queueLock, queue, user):
        """Create a scraper thread and set it running."""
        Thread.__init__(self)
        self.should_exit = False
        self.queueLock = queueLock
        self.queue = queue
        self.user = user
        self.job_id = job_id

    def run(self):
        """Continually try to scrape and save websites while there are jobs in the queue."""
        while not self.should_exit:
            self.queueLock.acquire()
            if not self.queue.empty():
                url = self.queue.get()
                self.queueLock.release()
                self.process_url(url)
            else:
                self.queueLock.release()
                time.sleep(1)

    def process_url(self, url):
        """Scrape and save a url and its scraping results."""
        try:
            scrape_and_save(url, self.user)
            self.add_result(url, True)
        except Exception as e:
            self.add_result(url, False, exception=e, trace=traceback.format_exc())

    def add_result(self, url, successful, exception=None, trace=None):
        """Add a result of a scraping job."""
        error_type = None
        error = None
        error_trace = None
        if exception:
            error_type = type(exception).__name__
            error = str(exception)
        if trace:
            error_trace = trace

        ScrapeResult.objects.create(job_id=self.job_id, source_url=url,
            successful=successful, error_type=error_type, error=error, error_trace=error_trace)
