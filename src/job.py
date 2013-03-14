#coding=utf8

import math
from datetime import datetime, timedelta



MIN_VALUES = {'year': 1970, 'month': 1, 'day': 1, 'week': 1,
              'day_of_week': 0, 'hour': 0, 'minute': 0, 'second': 0}
MAX_VALUES = {'year': 2 ** 63, 'month': 12, 'day': 31, 'week': 53,
              'day_of_week': 6, 'hour': 23, 'minute': 59, 'second': 59}
FIELDS = ['year', 'month', 'day', 'hour', 'minute', 'second']
FIELDS2 = ['days', 'seconds', 'minutes', 'hours', 'weeks']


def convert2datetime(dateval, format=None):
    if isinstance(dateval, float):
        dateval = int(dateval)
    if isinstance(dateval, int):
        return datetime.fromtimestamp(dateval)
    elif isinstance(dateval, basestring):
        if format is None:
            format = '%Y-%m-%d %H:%M:%S'
        return datetime.strptime(dateval, format)        
    elif isinstance(dateval, datetime):
        return dateval
    elif isinstance(dateval, date):
        return datetime.fromordinal(dateval.toordinal())

    return None


class Job(object):
    """docstring for Job"""
    def __init__(self, spider, project):
        super(Job, self).__init__()

        self._id = 'id' in spider and spider['id'] or spider['name']
        self._spider = spider['name']
        self._spider_params = params = {}

        # if 'start_urls' in spider:
        #     params['start_urls'] = spider['start_urls']

        # if 'allow_domain' in spider:
        #     params['allow_domain'] = spider['allow_domain']

        # if 'rules' in spider:
        #     params['rules'] = spider['rules']

        # if 'proxy' in spider:
        #     params['proxy'] = spider['proxy']

        # self._crawler_configs = configs = {}
        # configs['thread'] = spider.get('thread', 4)
        # configs['headers'] = spider.get('headers')

        self._init_sched(spider.get('sched'))

        self._project = project

        self._running = False
        self._count = 0

        self._next_tirgger = None



    @property
    def project(self):
        return self._project

    @property
    def running(self):
        return self._running

    @property
    def count(self):
        return self._count

    def _check_condition(self):
        pass

    def _init_sched(self, sched):
        self._sched_start_time = None
        self._sched_repeat = sched.get('repeat', None)
        if 'start_time' in sched:
            self._sched_start_time = convert2datetime(sched['start_time'])

        self._sched_config = {}
        if sched:
            self._sched_type = _sched_type = sched['type']
            if _sched_type == 'cron':
                for field in FIELDS:
                    self._sched_config[field] = sched.get(field, '*')
            elif _sched_type == 'interval':
                _deltap = {}
                for p in ['days', 'seconds', 'minutes', 'hours', 'weeks']:
                    if p in sched:
                        _deltap[p] = sched[p]
                self._sched_config['interval'] = timedelta(**_deltap)
                self._sched_config['length'] = self._sched_config['interval'].total_seconds()
                if sched.get('start_time', None) is None:
                    self._sched_start_time = datetime.now() + self._sched_config['interval']
        else:
            self._sched_type = None

    def _cron_next_tirgger(self, now):
        _next = now
        #if self._count == 0:
        #    return now
        #fields = FIELDS #['year', 'month', 'day', 'hour', 'minute', 'second']
        for i, field in enumerate(FIELDS):
            val = self._sched_config.get(field)
            if val is None or val == '*':
                continue
            cur = getattr(_next, field)
            kw = {}
            if cur > val and i > 0 and now > _next:
                j = i
                while j > 0:
                    _prev = FIELDS[j-1]
                    if self._sched_config.get(_prev) == '*':
                        kw[_prev] = getattr(_next, _prev) + 1
                        if kw[_prev] > MAX_VALUES[_prev]:
                            kw[_prev] = MAX_VALUES[_prev]
                        else:
                            break
                    j -= 1

            if cur != val:
                kw[field] = val
            if kw:
                _next = _next.replace(**kw)
        return _next

    def _interval_next_tirgger(self, now):
        num = math.ceil(((now - self._sched_start_time).total_seconds())/self._sched_config['length'])
        #delta = now - self._sched_start_time
        #delta_sec = delta.days * 3600 * 3600 * 24 + delta.seconds + delta.microseconds / 1000000.0
        #num = math.ceil(delta_sec / self._sched_config['length'])
        sec = self._sched_config['length'] * num
        _next = self._sched_start_time + timedelta(seconds=sec)
        return _next

    def _calc_next_tirgger(self, now):
        #now = datetime.now()
        print 'calc -> <%s> repeat: %s, count: %s now: %s, start: %s' % (self._id, self._sched_repeat, self._count, now, self._sched_start_time)

        if self._sched_repeat and self._sched_repeat < self._count:
            return None

        if self._sched_start_time and now < self._sched_start_time:
            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            return self._sched_start_time            

        if self._sched_type == 'cron':
            return self._cron_next_tirgger(now)
        elif self._sched_type == 'interval':
            return self._interval_next_tirgger(now)
        else:
            if self._count == 0:
                return now
            else:
                return None

    def calc_next_tirgger(self, now):
        self._next_tirgger = self._calc_next_tirgger(now)
        print '++++++++++++calc next -> [%s] %s' % (self._id, self._next_tirgger)
        return self._next_tirgger

    def get_next_tirgger(self):
        return self._next_tirgger

    def run(self):
        print ' --+++--> ', self._id, ' Im Running!!!!', datetime.now()
        def _on_finished():
            print ' --+++--> ', self._id, ' Im Finished!!!!'
            self._running = False
            self._count += 1

        self._running = True

        crawler = self._project.get_crawler()
        #crawler = Crawler(self._crawler_configs)
        #crawler.set_header(self._headers)
        spider = self._project.load_spider(self._spider)
        if spider:
            crawler.crawl(spider)
            crawler.add_callback(_on_finished)
        else:
            print 'Spider %s is not exists' % self._spider


