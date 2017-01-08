# -*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui
import sys, os, random, json, zlib
import urllib, urllib2, cookielib
import string, re, base64
import contact

SEP = os.sep
addonInfo = xbmcaddon.Addon ('plugin.video.burningseries')
dataPath = xbmc.translatePath(addonInfo.getAddonInfo('profile'))
addonPath = addonInfo.getAddonInfo('path')

urlHost = "http://bs.to/api/"
urlPics = "http://s.bs.to/img/cover/"

def getUrl(url):
	try:
		req = urllib2.Request(urlHost+url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		req.add_header('Accept-encoding', 'gzip')
		token_data = contact.do_token(url)
		req.add_header('BS-Token',token_data)
		response = urllib2.urlopen(req)
		if response.info().get('Content-Encoding') == 'gzip':
			d = zlib.decompressobj(16+zlib.MAX_WBITS)
			return d.decompress(response.read())
		else:
			return response.read()
		response.close()
	except:
		return False

pDialog = xbmcgui.DialogProgressBG()
pDialog.create('searchlist','refreshing')

data = getUrl("series")
jsonContent = json.loads(data)
items = len(jsonContent)
pos = 0

print "[bs] items search "
print items

w = open(dataPath+SEP+"searchList.data","wb")
w.write('')
w.close()

pDialog.update(pos)
out = u""
for d in jsonContent:
	pos = pos + 1
	out = d['series'].strip().encode('utf-8')+"|".encode('utf-8')+d['id'].encode('utf-8')+'\n'.encode('utf-8')
	val = int(100*pos/items)
	pDialog.update(val)
	with open (dataPath+SEP+"searchList.data", 'a') as f: 
		f.write (out)
	
print "[bs] pos val"
print out

pDialog.close();

xbmc.executebuiltin("Notification(searchList,success,2000)")


