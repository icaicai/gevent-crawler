#coding=utf8

import urlparse
from urllib2 import _parse_proxy
from lxml import html
from downloader import Request

class Spider(object):
    """docstring for Spider"""

    start_urls = set()
    allow_domain = None
    #rules = []
    proxy = None
    crawler = None
    _proxy_config = None

    def __init__(self):
        super(Spider, self).__init__()

    def set_params(self, **kw):
        for key, val in kw.items():
            if key in ('start_urls', 'allow_domain', 'rules', 'proxy'):
                setattr(self, key, val)

    def pre_requests(self):
        if self.proxy:
            self._proxy_config = {}
            proxy_type, user, password, hostport = _parse_proxy(self.proxy)
            if user and password:
                user_pass = '%s:%s' % (unquote(user), unquote(password))
                creds = base64.b64encode(user_pass).strip()
                self._proxy_config['creds'] = creds
            hostport = unquote(hostport)
            self._proxy_config['hostport'] = hostport
            self._proxy_config['proxy_type'] = proxy_type
                        

    def start_requests(self):
        self.pre_requests()
        reqs = map(self.make_request, self.start_urls)
        return reqs

    def make_request(self, url):
        req = Request(url)
        if self._proxy_config:
            if 'creds' in self._proxy_config
                req.add_header('Proxy-authorization', 'Basic ' + self._proxy_config['creds'])
            req.set_proxy(self._proxy_config['hostport'], self._proxy_config['proxy_type'] or req.get_type())
        return req
        
    def process(self, responses):
        for res in responses:
            if not res:
                continue
            try:
                results = self.parse(res)
                results = self.filter(results)
                self.pipeline(results)
            except:
                import traceback
                traceback.print_exc()
        self.crawler.finish(self)

    def parse(self, res):
        '''解析抓取来的内容'''
        return []


    def filter(self, items):
        '''过滤解析后，得到的数据'''
        return items
        #for rule in self.rules:
        #    items = filter(rule.valid, items)
        #return items

    def pipeline(self, items):
        '''数据后续处理'''
        return items  

    def get_xmldoc(self, text):
        '''返回lxml的Document对象'''
        return html.document_fromstring(text)


class LinkSpider(Spider):
    """docstring for LinkSpider"""

    def parse(self, res):
        urls = set()
        doc = self.get_xmldoc(res.text)
        doc.make_links_absolute(doc.base_url or res.url)
        for el, attr, link, pos in doc.iterlinks():
            if el.tag == "a":
                if '#' in link:
                    link = link[:link.index('#')]
                if self.allow_domain:
                    pr = urlparse.urlparse(link)
                    if pr.netloc == self.allow_domain:
                        urls.add(link)
                else:
                    urls.add(link)
        return urls