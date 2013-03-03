#coding=utf8

"""\
各种过滤规则
"""


class Rule(object):
    """docstring for Rule"""
    def __init__(self, arg):
        super(Rule, self).__init__()
        self.arg = arg


class LinkRule(Rule):
    """docstring for LinkRule"""
    def __init__(self, arg):
        super(LinkRule, self).__init__()
        self.arg = arg
        
class TextRule(object):
    """docstring for TextRule"""
    def __init__(self, arg):
        super(TextRule, self).__init__()
        self.arg = arg
                        
