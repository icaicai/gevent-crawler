#coding=utf8


from downloader import Downloader

class Crawler(object):

    def __init__(self, configs):
        thread = configs.get('thread', 4)
        retry = configs.get('retry', 3)
        headers = configs.get('headers')
        self._downloader = Downloader(thread, retry)
        if headers:
            self._downloader.add_headers(headers)

        self._spiders = []
        self._callbacks = []

    def add_callback(self, func):
        self._callbacks.append(func)

    def _finished(self):
        for func in self._callbacks:
            try:
                func()
            except Exception, e:
                pass

    def finish(self, spider):
        if spider in self._spiders:
            self._spiders.remove(spider)
            if not self._spiders:
                self._finished()

    def crawl(self, spider):
        self._spiders.append(spider)
        spider.crawler = self
        requests = spider.start_requests()
        g = self._downloader.fetch(requests)
        g.link(spider.process)
        #g.link(_on_finished)
