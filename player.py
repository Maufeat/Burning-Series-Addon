# -*- coding: utf-8 -*-
import xbmc
from watched import *

class bsPlayer(xbmc.Player):
	def __init__( self, *args, **kwargs ):
		xbmc.Player.__init__( self )

	def playStream(self, url, n, season, episode):
		print "[bs][player.py] playStream"
		self.play(url)
		name = n.decode('utf-8')
		done = False
		if readWatchedData(name.encode('utf-8')+"/"+season+"/"+episode):
			done = True
		while (not xbmc.abortRequested and self.isPlaying()):
			totalTime = self.getTotalTime()
			tRemain =  totalTime - self.getTime()
			if totalTime<60:
				relativeWatched = 5
			else:
				relativeWatched = 10
			if tRemain<(totalTime/100*relativeWatched) and not done:
				print "[bs][playStream] marked as watched :"+name.encode('utf-8')+"/"+season+"/"+episode
				writeWatchedData((name+"/"+season+"/"+episode).encode('utf-8'))
				done = True
			xbmc.sleep(2000)

	def onPlayBackStarted(self):
		print "[bs][bsPlayer] PLAYBACK STARTED"
    
	def onPlayBackEnded(self):
		print "[bs][bsPlayer] PLAYBACK ENDED"

	def onPlayBackStopped(self):
		print "[bs][bsPlayer] PLAYBACK STOPPED"