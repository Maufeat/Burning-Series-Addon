#-*- coding:utf-8 -*-
import sys, os, md5
import xbmc, xbmcaddon, xbmcplugin

# inspiration and codepieces
# written by 0xC001 (bs.to forum)
# -- 01.09.2015

# -- let the games begin --
sp = os.sep
spi = xbmcaddon.Addon ('plugin.video.burningseries')
MAIN = spi.getAddonInfo('path')+sp
DATA = MAIN.replace('addons'+sp+'plugin.video.burningseries', 'addon_data'+sp+'plugin.video.burningseries')
CACHE = DATA+"cache"+sp

core.mkdir(CACHE)
cookieJar = ""

# --
def login(username, password):
	import lib.web as web
	global MAIN
	
	cacheDays = 4;

	if not os.path.isfile(MAIN+'session'):
		open(MAIN+'session', 'a').close()
	
	if isCacheValid(MAIN+'session', cacheDays) == False:
		os.remove(MAIN+'session')
		open(MAIN+'session', 'a').close()
	
	fd = open(MAIN+'session','r+')
	session = fd.read()
	if session != "":
		fd.close()
		return session
		
	if(username == "" or password == ""):
		return ""
	inhalt = web.postPage("http://bs.to/api/login/", "login[user]="+username+"&login[pass]="+password)
	print '##'
	print inhalt
	print '###'
	data = json.loads(inhalt, 'UTF-8')
	if "session" in data:
		fd.write("?s="+data["session"])
		fd.close()
		return "?s="+data["session"]
	elif "error" in data:
		line1 = "Fehler!"
		line2 = data["error"]
		xbmcgui.Dialog().ok(line1, line2)

def getFavorites():
	url = "http://bs.to/api/user/series"
	daten = getPage(url)
	return daten

def setFavorites(ids):
	url = "http://bs.to/api/user/series/set/"+(','.join(ids))
	daten = json.loads(getPage(url), 'UTF-8')
	return daten
	
# --- helper from core --

def isCacheValid(file, days):
	import time
	if(isFile(file)):
		return (time.time() - os.path.getmtime(file) < (days * (24 * 3600)))
	else:
		return False

# --- helper from web --

def getPage(url, showMessage = True, cookies = False):
	global cookieJar
	if(showMessage):
		handle = int(sys.argv[1])
		username=xbmcplugin.getSetting(handle, 'username')
		password=xbmcplugin.getSetting(handle, 'password')
		logged = login(username, password)
		if logged is not None:
			url = url+login
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0')
		if(cookies == True):
			req.add_header('Cookie', cookieJar)
		response = urllib2.urlopen(req)
		if(cookies == True):
			cookieJar = response.info().getheader('Set-Cookie')
				
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read()
			
		response.close()
		return data
	except urllib2.URLError, e:
		if showMessage:
			line1 = "Fehler!"
			line2 = "bs.to nicht erreichbar"
			xbmcgui.Dialog().ok(line1, line2)
			sys.exit()
		return ""
		
def postPage(url, daten, cookies = False):
	global cookieJar
	
	if type(daten) is list:
		daten=urllib.urlencode(daten)
		print daten
	
	print type(daten)
	req=urllib2.Request(url, daten)
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0')
	if(cookies == True):
		req.add_header('Cookie', cookieJar)
	
	response = urllib2.urlopen(req)
	
	if(cookies == True):
		cookieJar = response.info().getheader('Set-Cookie')

	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO( response.read())
		f = gzip.GzipFile(fileobj=buf)
		data = f.read()
	else:
		data = response.read()
	response.close()
	
	return data
