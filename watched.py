# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import os, sys, shutil

SEP = os.sep
thisPlugin = int(sys.argv[1])
addonInfo = xbmcaddon.Addon()
dataUrl = xbmc.translatePath(addonInfo.getAddonInfo('profile'))
oldWatchedPath = addonInfo.getAddonInfo('path')
watchedFile = dataUrl+SEP+"watched.data"

# since 1.3.0
def writeWatchedData(n):
	global watchedFile
	name = n
	f = xbmcvfs.File(watchedFile)
	d = f.read()
	f.close()
	f = xbmcvfs.File(watchedFile, 'w')
	b = d+name+"\n"
	result = f.write(b)
	print "[bs][writeWatchedData] write "+watchedFile+" -> "+ name
	f.close()
	return result
	
def readWatchedData(n):
	global watchedFile
	name = n
	f = xbmcvfs.File(watchedFile)
	b = f.read()
	f.close()
	watchedData = b.splitlines()
	for m in watchedData:
		if name == m:
			print "[bs][readWatchedData] found "+name+" in watched.data"
			return True
	print "[bs][readWatchedData] "+name+" not found in watched.data"
	return False

def changeToWatched(watchedString):
	# -- rewrite listentry
	global thisPlugin
	color = xbmcplugin.getSetting(thisPlugin, 'watchedColor')
	return "[COLOR "+color+"]w [I]"+watchedString+"[/I][/COLOR]"

def markParentEntry(urlData):
	if not readWatchedData(urlData):
		writeWatchedData(urlData)

def checkUserPath():
	global dataUrl,watchedFile,oldWatchedPath,SEP
	print "[bs][watched] checkUserPath"
	if not os.path.exists(dataUrl):
		os.makedirs(dataUrl)
	if not os.path.exists(watchedFile):
		if os.path.exists(oldWatchedPath+SEP+"watched.data"):
			print "[bs][watched] migrating data to:"
			print watchedFile
			shutil.copy(oldWatchedPath+SEP+"watched.data",watchedFile)
		else:
			print "[bs][watched] creating:"
			print watchedFile
			file = open(watchedFile, 'w+')