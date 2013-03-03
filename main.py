#coding=utf8

import sys
import os.path
import gevent
from gevent import monkey
monkey.patch_all()


sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scheduler import Scheduler



if __name__ == '__main__':
    sched = Scheduler()
    curr_dir = os.path.dirname(__file__)
    proj_path = os.path.join(curr_dir, 'projects')
    sched.load_projects(proj_path)
    sched.start()
    gevent.wait()
