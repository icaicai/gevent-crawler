#coding=utf8

from spider import Spider, LinkSpider
import db

class Entry(Spider):

    def parse(self, res):
        print 'Entry.parse'
        
        #doc = html.document_fromstring(text)
        doc = self.get_xmldoc(res.text)
        cats = doc.body.findall(".//div[@id='protal_list']//div[@class='item']")
        links = []
        for cat in cats:
            _e = cat.find("div[@class='item_hd']//a")
            #_1 = _e.text
            for dl in cat.findall('.//dl'):
                _2 = dl.find('dt').text

                for a in dl.findall('dd/a'):
                    href = a.attrib['href']
                    name = a.text
                    links.append((href, name))
                    #print (href, name)
                    #print >> fp, href, name.encode('utf8')
        return links[:2]


    def filter(self, items):
        return items
        #print items
        print 'Entry ^^^ filter'

    def pipeline(self, items):
        print 'Entry ^^^ pipline'
        if items:
            for c in items:
                cat = Category(c[1], c[0])
                #cat.urls = [c[0]]
                self.crawler.crawl(cat)
            #urlManager.add_urls(items, self.crawler.name)


class Category(Spider):


    def __init__(self, name, url):
        super(Category, self).__init__()
        self._name = name
        self.start_urls = [url]


    def parse(self, res):
        doc = self.get_xmldoc(res.text)
        doc.make_links_absolute(doc.base_url or res.url)
        lis = doc.body.findall(".//ul[@class='list_goods']/li[@class='item_list']")
        links = []
        for li in lis:
            a = li.find(".//h4[@class='link_name']/a")
            title = a.text
            url = a.attrib['href']
            links.append(url)
        #next page
        page = doc.body.find(".//div[@class='paginator']")

        if page is not None:
            cur = page.find("span[@class='page-this']")
            if cur is not None:
                nxt = cur.getnext()
                if nxt is not None and nxt.tag == 'a':
                    print 'next page'
                    url = nxt.attrib['href']
                    #links.append(url)
                    print url
                    cat = Category(self._name, url)
                    #cat.urls = []
                    self.crawler.crawl(cat)
        return links


    def pipeline(self, items):
        print '->Category crawl', self._name, len(items)
        if items:
            p = Product(self._name)
            p.start_urls = items
            self.crawler.crawl(p)            


class Product(Spider):

    def __init__(self, cat=None):
        super(Product, self).__init__()
        self._cat = cat

    def pre_requests(self):
        super(Product, self).pre_requests()
        if not self.start_urls:
            print '>> start url from db <<'
            self.start_urls = db.get_urls()

    def parse(self, res):
        #urlManager.touch(res.url) #
        #print 'Product.parse --> ', res.url

        doc = self.get_xmldoc(res.text)
        #scripts = doc.head.findall('script/text()')
        #title = doc.head.find('title').text
        #for sc in scripts:
        #    if 'window.pageConfig' in sc:
        #        txt = sc
        box = doc.body.xpath(".//div[contains(@class, 'property id_promotion')]")
        t = box[0].find("h1")
        title = t.text
        s = box[0].find(".//strong[@class='price_font']")
        price = s.text
        #print title, price
        #li class="li promotion"促销
        #a  class="tags_promo tags_promo_songquan" 促销内容
        #a class="btn_notice" 缺货
        #a class="btn_cart" 购买
        #a id="btn_installment" 分期


        data = {}
        data['url'] = res.url
        data['title'] = title
        data['price'] = price
        data['category'] = self._cat
        #self.store.save(data) 
        db.save_goods(data)        