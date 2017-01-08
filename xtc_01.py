# -*- coding: utf-8 -*-
import base64
import time
import hmac
import hashlib
import base64
import json


def do_token(unlustig):
	fme = ghz(hud)
	lk = { "public_key": str(fme['pk']), "timestamp": "000", "hmac": "hHinB7fFhutVr4dAP0MLThg16E"}
	derbe = int(time.time())
	strmh = str(derbe)+"/"+unlustig
	cdmh = hmac.new(fme['kp'], msg=strmh, digestmod=hashlib.sha256).hexdigest()
	lk['timestamp'] = str(derbe)
	lk['hmac'] = str(cdmh)
	ecdjs = json.dumps(lk, ensure_ascii=False)
	return base64.b64encode(ecdjs)

def ghz(efg):
	lD = efg['sx']
	le = efg['sz']
	lt = efg['sf']
	lr = efg['sh']
	i = 0
	gkk = {"kp": "","pk":""}
	while i<len(lD):
		gkk['kp'] = gkk['kp'] + str(unichr(lD[i]+12)) + str(unichr(le[i]+10))
		gkk['pk'] = gkk['pk'] + str(unichr(lt[i]+13)) + str(unichr(lr[i]+9))
		i+=1
	return gkk