#coding=utf8

import os
import os.path
import gevent
import loader
from datetime import datetime
from project import Project
from job import Job


class Scheduler(object):
    """docstring for Scheduler"""
    def __init__(self):
        super(Scheduler, self).__init__()

        self._thread = None
        self._projs = {}
        self._jobs = []

    def load_projects(self, path):
        self._projs = {}
        for fn in os.listdir(path):
            if fn in ('.', '..'): continue
            proj_path = os.path.join(path, fn)
            if os.path.isdir(proj_path):
                config_file = os.path.join(proj_path, 'configs.py')
                if os.path.exists(config_file):
                    cfg = loader.load_module(config_file)
                    if cfg:
                        proj = Project(cfg, proj_path)
                        name = hasattr(cfg, 'name') and cfg.name or fn
                        self._projs[name] = proj

        self.load_jobs()

    def load_jobs(self):
        for name, proj in self._projs.iteritems():
            configs = proj.configs
            if 'spiders' in configs:
                for spider in configs['spiders']:
                    job = Job(spider, proj)
                    self._jobs.append(job)
                    #if 'sched' in spider:
                    #    pass

    def add_job(self, job):
        self._jobs.append(job)


    def start(self):
        now = datetime.now()
        for job in self._jobs:
            job.calc_next_tirgger(now)
        self._thread = gevent.spawn(self._run)

    def stop(self):
        for job in self._jobs:
            job.stop()
        self._thread.join()

    def _run_job(self, job):
        gevent.spawn(job.run)

    def _run(self):
        now = datetime.now()
        finished = []
        _next = None
        for job in self._jobs:
            wakeup = job.get_next_tirgger()
            print ' wakeup++> <%s> %s %s' % (job._id, now, wakeup)
            if wakeup is None:
                finished.append(job)
            else:
                if wakeup <= now:
                    self._run_job(job)
                
                _next_wakeup = job.calc_next_tirgger(now)
                if _next_wakeup and (_next is None or _next_wakeup < _next):
                    _next = wakeup
                
                

        print '------------Next Run -> ', _next
        for job in finished:
            self._jobs.remove(job)

        if _next:
            t = (_next-now).total_seconds()
            self._thread = gevent.spawn_later(t, self._run)
