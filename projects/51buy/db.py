#coding=utf8

import time
from store import store

_c_goods = store.get_collection('51buy')


def get_urls():
    us = _c_goods.find(fields=['url'])
    urls = [u['url'] for u in us]
    return urls


def save_goods(data):
    url = data.get('url')
    title = data.get('title')
    price = float(data.get('price', 0.0))
    category = data.get('category')
    #print '--> ', data
    if not url:
        return

    if 'prices' in data:
        del data['prices']

    g = _c_goods.find_one({'url':unicode(url)})

    if g:
        prices = g.get('prices')
        if prices:
            last_price = prices[len(prices)-1]
            last_price['price'] = float(last_price['price'])
    else:
        g = data
        prices = None

    if not prices:
        last_price = {}
        last_price['price'] = price
        last_price['begin'] = last_price['end'] = time.time()
        prices = []
        prices.append(last_price)
        g['prices'] = prices

    if last_price['price'] != price:
        last_price['end'] = time.time()
        lp = dict(price=data['price'], begin=time.time(), end=time.time())
        prices.append(lp)

        g['delta'] = price - last_price['price']
    g['updated'] = time.time()

    _c_goods.save(g)    
