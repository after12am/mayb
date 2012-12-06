import os, sys, re, time, urllib
import lxml.html
from utils.charset import to_unicode, to_unicode_if_htmlentity
from datetime import datetime
from db.mapper import Pins, Words

script_regx = re.compile('<script.*?/script>', re.DOTALL)
noscript_regx = re.compile('<noscript.*?/noscript>', re.DOTALL)
style_regx = re.compile('<style.*?/style>', re.DOTALL)
iframe_regx = re.compile('<iframe.*?/iframe>', re.DOTALL)
select_regx = re.compile('<select.*?/select>', re.DOTALL)
comment_regx = re.compile('<!--.*?-->', re.DOTALL)

class _HTML(object):
    
    def __init__(self):
        self.req = None
        self.dom = None
    
    def request(self, url):
        try:
            self.req = urllib.urlopen(url)
        except:
            # unable to download
            # something error has happened.
            return 0
        doc = self.clean(to_unicode(self.req.read()))
        try:
            self.dom = lxml.html.fromstring(doc)
        except:
            # something error has happened by lxml.html.
            return 0
        return self.req.getcode()
    
    def clean(self, doc):
        doc = to_unicode_if_htmlentity(doc)
        doc = script_regx.sub('', doc)
        doc = noscript_regx.sub('', doc)
        doc = style_regx.sub('', doc)
        doc = iframe_regx.sub('', doc)
        doc = select_regx.sub('', doc)
        doc = comment_regx.sub('', doc)
        return doc

class _Pin(_HTML):
    
    def __init__(self):
        super(_Pin, self).__init__()
    
    def get_image_id(self):
        e = self.dom.cssselect('a.like_pin[data-id]')[0]
        return e.get('data-id')
    
    def get_image(self):
        try:
            e = self.dom.get_element_by_id('pinCloseupImage')
            return e.get('src')
        except KeyError:
            return False
    
    def get_refer_url(self):
        try:
            e = self.dom.get_element_by_id('pinCloseupImage').getparent()
            return e.get('href')
        except KeyError:
            return False
    
    def get_description(self):
        e = self.dom.get_element_by_id('PinCaption').cssselect('.description')[0]
        if e.text:
            return e.text
        else:
            return ''
    
    def get_repin_story(self):
        return self.dom.get_element_by_id('PinRepins').cssselect('.PinRepinStory')
    
    def get_repins(self):
        repins = {}
        for e in self.get_repin_story():
            # user who repins
            user = re.compile(r'/([\w]*)/').findall(e.cssselect('.CommenterImage')[0].get('href'))[0]
            repins.setdefault(user, {})
            # words to mark
            text = e.cssselect('.repin_post_attr a')[1].text
            if not text:
                continue
            words = re.compile('[\w]*').findall(text.lower())
            words = [w for w in words if len(w) > 3]
            for w in list(set(words)):
                repins[user].setdefault(w, words.count(w))
        return repins
    
    def save(self):
        id = self.get_image_id()
        if not id:
            return 0
        pins = Pins()
        pins.data['pin_id'] = id
        pins.data['image_url'] = self.get_image()
        pins.data['description'] = self.get_description()
        pins.data['refer_url'] = self.get_refer_url()
        if not pins.save():
            return 0
        repins = self.get_repins()
        wordcount = {}
        for user in repins:
            words = Words()
            words.data['pin_id'] = id
            words.data['user'] = user
            # delete and insert in preperation for change of board name.
            words.delete()
            for w in repins[user]:
                words.data['word'] = w
                words.save()
        return 1

page = {
    'home': 'http://pinterest.com',
    'popular': 'http://pinterest.com/popular/'
}

def _get_populars():
    try:
        popular_doc = _HTML()
        if popular_doc.request(page['popular']) == 200:
            populars = popular_doc.dom.cssselect('.PinHolder .PinImage')
            return [page['home'] + popular.get('href') for popular in populars]
    except:
        print '[%s] Failed to download. %s' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), page['popular'])
    return []

def crawle(sleep=60):
    while True:
        for url in _get_populars():
            print '[%s] Get from %s ' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), url)
            pin = _Pin()
            if pin.request(url) == 200:
                if pin.save():
                    print '[%s] Success!' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'),)
                else:
                    print '[%s] Failed to save to database.' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'),)
            else:
                print '[%s] Failed to download.' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'),)
        time.sleep(sleep)

def main():
    crawle()

if __name__ == '__main__': main()