"""Processes the jobs created by a batch request."""

from threading import Thread, Lock
from queue import Queue
import time
from .scraper_functions import get_batch
from .utils import scrape_and_save
from .errors import UnknownWebsiteError, RecipeParsingError
from urllib.error import URLError

_wrapper_thread_counter = 1

def submit_job(urls, begin, end, user):
    """Submit a job on a separate thread."""
    global _wrapper_thread_counter
    thread = WrapperThread(urls, begin, end, user)
    thread.daemon = True
    thread.name = "WrapperThread-{}".format(_wrapper_thread_counter)
    _wrapper_thread_counter += 1
    thread.start()

class WrapperThread(Thread):
    """Creates a job processor on a new thread."""

    def __init__(self, urls, begin, end, user):
        """Create a wrapper thread to start the job processor."""
        Thread.__init__(self)
        self.urls = urls
        self.begin = begin
        self.end = end
        self.user = user

    def run(self):
        """Create a JobProcessor on a new thread."""
        processor = JobProcessor(4, self.user)
        processor.add_jobs(self.urls, self.begin, self.end)
        processor.wait()
        print("Done with job")

class JobProcessor():
    """Manages the processing of a set of jobs."""

    def __init__(self, num_threads, user):
        """Create a JobProcessor with the specified number of threads."""
        self.queue = Queue()
        self.queueLock = Lock()
        self.threads = []
        for i in range(1, num_threads + 1):
            self.threads.append(ScraperThread(self.queueLock, self.queue, user))

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

    def __init__(self, queueLock, queue, user):
        """Create a scraper thread and set it running."""
        Thread.__init__(self)
        self.should_exit = False
        self.queueLock = queueLock
        self.queue = queue
        self.user = user

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
            print("Saved url: {}".format(url))
        except (URLError) as e:
            print('Invalid url: ' + str(e))
        except (KeyError, ValueError) as e:
            print('Key or Value error: ' + str(e))
        except UnknownWebsiteError as e:
            print('Unknown website: ' + str(e))
        except RecipeParsingError as e:
            print('{0} -- Recipe parsing error: {1}'.format(url, e))
