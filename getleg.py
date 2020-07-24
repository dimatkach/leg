#!/usr/bin/env python3

from urllib3 import PoolManager
import json
import re
import sys

root='https://openstates.org/'

http=PoolManager()

def get(url): return str(http.request('GET', url).data)

def get_list(url):
   html=get(url)
   pattern = r'^.*window.legislators\s*=\s*(\[.+?\]);.*$'
   js=re.sub(pattern, r'\1', html, flags=re.S)
   return json.loads(re.sub(r'\\', '', js))

def get_state(state): return get_list("%s/%s/legislators/" % (root, state))

def enrich(js):
   url = js['pretty_url']
   html = get('%s/%s' % (root, url))
   email = re.sub(r'^.*mailto:(.+?)">.*$', r'\1', html, flags=re.S)
   surname = re.sub(r',*$', '', js['name']).split(' ').pop()
   salutation = 'Dear %s %s' % (js['current_role']['role'], surname)
   js['email'] = email
   js['surname'] = surname
   js['salutation'] = salutation
   return js


state=sys.argv[1]
list=get_state(state)
for r in list: enrich(r)

print(json.dumps(list))

