#!/usr/bin/python
import os, sys, cgi, json, site

site.addsitedir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../core'))

from db.mapper import Pins

if 'QUERY_STRING' in os.environ:
    query = cgi.parse_qs(os.environ['QUERY_STRING'])
else:
    query = {}

def get_candidates(offset=0, num=20, threshold=0.5):
    pins = Pins()
    pins = pins.get_candidates(offset, num, threshold)
    return [{'pin_id':str(pin[0]), 'uri':str(pin[1])} for pin in pins]

print "Content-Type: text/json\n\n"
print json.dumps(get_candidates(int(query['offset'][0]), int(query['n'][0])))