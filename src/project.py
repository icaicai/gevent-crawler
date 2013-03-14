#coding=utf8

import os
import os.path
import loader
from downloader import Downloader
from crawler import Crawler
from spider import LinkSpider

class Project(object):
    """docstring for Project"""
    def __init__(self, configs, path):
        super(Project, self).__init__()
        self.name = 'name' in configs and configs['name'] or os.path.basename(path)
        self.configs = configs['configs']
        self._path = path
        self._spiders_cls = {}
        self._spiders_cfg = {}

        if 'spiders' in self.configs:
            cfgs = self.configs['spiders']
            for scfg in cfgs:
                name = scfg.get('id') or scfg.get('name')
                self._spiders_cfg[name] = scfg

        self._downloader = None


    def load_spider(self, name, params=None):
        spider_cls = None
        if name in self._spiders_cls:
            spider_cls = self._spiders_cls[name]
        else:
            for fn in os.listdir(self._path):
                if fn in ('.', '..'): continue
                fp = os.path.join(self._path, fn)
                if os.path.isfile(fp):
                    mod = loader.load_module(fp)
                    if mod and name in mod:
                        spider_cls = mod[name]
                        self._spiders_cls[name] = spider_cls

        if spider_cls:
            s = spider_cls()
            p = self._spiders_cfg.get(name, {})
            if params:
                p.update(params)
            if p:
                s.set_params(**p)
            
            return s

        return None

    def get_downloader(self):
        if self._downloader is None:
            thread = self.configs.get('thread', 4)
            headers = self.configs.get('headers')
            self._downloader = Downloader(thread)
            if headers:
                self._downloader.add_headers(headers)

        return self._downloader

    def get_crawler(self):
        crawler = Crawler(self)
        return crawler

