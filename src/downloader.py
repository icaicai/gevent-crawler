#coding=utf8

import urllib2
from gevent import pool

class Request(urllib2.Request):
    pass

        
class Response(object):
    """docstring for Response"""
    def __init__(self, resp):
        super(Response, self).__init__()
        self._resp = resp
        self._txt = None
        self.code = resp.code
        self.reason = resp.msg
        self.url = resp.url

    @property
    def text(self):
        if self._txt is not None:
            return self._txt

        self._txt = self._resp.read()
        if type(self._txt) is str:
            try:
                self._txt = self._txt.decode('gbk')
            except:
                pass
        
        return self._txt

    def get_header(self, name):
         return self._resp.headers.get(name)

    def get_headers(self):
        return self._resp.headers.dict





class Downloader(object):
    """docstring for Downloader"""
    def __init__(self, thread, retry=3):
        super(Downloader, self).__init__()

        self._pool = pool.Pool(thread)
        self._retry = retry
        self._headers = {}

        self._dl_urls = set() #抓取中的url

        self._opener = urllib2.build_opener()

    def add_header(self, key, val):
        self._headers[key] = val

    def add_headers(self, headers):
        self._headers.update(headers)

    def fetch(self, reqs):
        g = self._pool.imap_unordered(self._download, reqs)
        return g

    def _download(self, req):
        for key, val in self._headers.iteritems():
            req.add_header(key, val)

        if req.get_full_url() in self._dl_urls:
            return

        self._dl_urls.add(req.get_full_url())
        res = self._opener.open(req)

        return Response(res)
