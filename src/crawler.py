#coding=utf8


class Crawler(object):

    def __init__(self, proj):
        self._proj = proj
        self._downloader = proj.get_downloader()
        self._running_spiders = []
        self._callbacks = []

    def get_spider(self, name, params=None):
        return self._proj.get_spider(name, params)

    def add_callback(self, func):
        self._callbacks.append(func)

    def _finished(self):
        for func in self._callbacks:
            try:
                func()
            except Exception, e:
                pass

    def finish(self, spider):
        if spider in self._running_spiders:
            self._running_spiders.remove(spider)
            if not self._running_spiders:
                self._finished()

    def crawl(self, spider):
        self._running_spiders.append(spider)
        spider.crawler = self
        requests = spider.start_requests()
        g = self._downloader.fetch(requests)
        g.link(spider.process)
        #g.link(_on_finished)
