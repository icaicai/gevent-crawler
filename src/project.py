#coding=utf8

import os
import os.path
import loader
from spider import LinkSpider

class Project(object):
    """docstring for Project"""
    def __init__(self, configs, path):
        super(Project, self).__init__()
        self.name = 'name' in configs and configs['name'] or os.path.basename(path)
        self.configs = configs['configs']
        self._path = path
        self._cls_spiders = {}

    def load_spider(self, name, params=None):
        spider_cls = None
        if name in self._cls_spiders:
            spider_cls = self._cls_spiders[name]
        else:
            for fn in os.listdir(self._path):
                if fn in ('.', '..'): continue
                fp = os.path.join(self._path, fn)
                if os.path.isfile(fp):
                    mod = loader.load_module(fp)
                    if mod and name in mod:
                        spider_cls = mod[name]
                        self._cls_spiders[name] = spider_cls

        if spider_cls:
            s = spider_cls()
            if params:
                s.set_params(**params)
            
            return s

        return None

