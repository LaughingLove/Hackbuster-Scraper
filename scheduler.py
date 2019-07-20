from __future__ import print_function
from threading import Timer


import hackbuster_scraper



class RepeatingTimer(object):

    def __init__(self, interval, f, *args, **kwargs):
        self.interval = interval
        self.f = f
        self.args = args
        self.kwargs = kwargs

        self.timer = None

    def callback(self):
        self.f(*self.args, **self.kwargs)
        self.start()

    def cancel(self):
        self.timer.cancel()

    def start(self):
        self.timer = Timer(self.interval, self.callback)
        self.timer.start()

class hackbuster_scheduler():
    def __init__(self):
        self.indicator = False
        self.initial_text = hackbuster_scraper.HackbusterScraper().get_article_text_brief()
    
    def check(self):
        new_text = hackbuster_scraper.HackbusterScraper().get_article_text_brief()
        if self.initial_text is not new_text:
            self.indicator = True
            return
        else:
            return
    
    def start_timer(self):
        while not self.indicator:
            t = RepeatingTimer(1800, self.check())
            t.start()
            print("Restarted!")



