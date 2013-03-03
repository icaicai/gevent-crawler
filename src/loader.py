#coding=utf8

"""\
用于加载
"""
import sys
import os
import os.path
import imp
import marshal


def load_module(filename, globals_=None):
    try:
        if globals_ is None:
            globals_ = {}
        sys.path.append(os.path.dirname(filename))
        #类型猜测
        type = None
        code = None
        root, ext = os.path.splitext(filename)
        for suf in imp.get_suffixes():
            if ext == suf[0]:
                type = suf[2]
                break

        if type == imp.PY_SOURCE:
            fp = open(filename, 'rU')
            code = fp.read()
        elif type == imp.PY_COMPILED:
            fp = open(filename, 'rb')
            magic = fp.read(4)
            if magic != imp.get_magic():
                return None
            fp.read(4) # Skip timestamp
            code = marshal.load(fp)
        if code is not None:
            exec(code, globals_)
            #if '__builtins__' in globals_:
            #    del globals_['__builtins__']
            return globals_
    except Exception, e:
        raise e
    finally:
        sys.path.remove(os.path.dirname(filename))