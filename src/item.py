#coding=utf8


class Item(object):
    """docstring for Item"""
    def __init__(self, arg):
        super(Item, self).__init__()
        self.arg = arg

class TextItem(Item):
    """docstring for TextItem"""
    def __init__(self, arg):
        super(TextItem, self).__init__()
        self.arg = arg
        
class IntItem(object):
    """docstring for IntItem"""
    def __init__(self, arg):
        super(IntItem, self).__init__()
        self.arg = arg
                        