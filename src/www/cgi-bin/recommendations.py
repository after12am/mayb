#!/usr/bin/python
import os, sys, cgi, json, site

site.addsitedir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../core'))

from db.mapper import Pins, Clusters

if 'QUERY_STRING' in os.environ:
    query = cgi.parse_qs(os.environ['QUERY_STRING'])
else:
    query = {}

clusters = Clusters()
pins = clusters.get_top_matches(query['pin_id'][0], 50, 0.5)
res = [{'score':str(pin[0]), 'uri':str(pin[2]), 'pin_id': str(pin[3])} for pin in pins]

print "Content-Type: text/json\n\n"
print json.dumps(res)