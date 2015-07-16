import os
import redis
import uuid
import json
from socket import gethostname, gethostbyname 
import time
#time.ctime() # 'Mon Oct 18 13:35:29 2010'

from flask import Flask, request, render_template



app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"
counter=0
COLOR = BLUE
services = os.getenv("VCAP_SERVICES")


services_info = json.loads(services)
hostname = services_info['rediscloud'][0]['credentials']['hostname']
password = services_info['rediscloud'][0]['credentials']['password']
port = services_info['rediscloud'][0]['credentials']['port']
COLOR = BLUE
r = redis.StrictRedis(host=hostname, port=port, db=0, password=password)

@app.route('/')
def hello():
	ip=request.headers.getlist("X-Forwarded-For")[0]
	r.incr('andrey-counter')
	usrtime = time.strftime('%l:%M%p %Z on %b %d, %Y')
	r.rpush('andrey-ips2',usrtime + ' ' +ip+'<br>')
	mylist=r.lrange('andrey-ips2',0,-1)
	nlist=''
	for i in mylist:
	 nlist=nlist+i
	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Hi, I'm GUID:{}<br/>
	
	</center>
	<center>This page has been visited {} times</center>
	<center><h1><font color="red">Your IP is detected and logged: {}<br/>

	
<h5><font color="white">
Visitor's list:<br>
{}
</center>
	
	</body>
</html>
	""".format(COLOR,my_uuid,r.get('andrey-counter'), ip,nlist)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
	#app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))
