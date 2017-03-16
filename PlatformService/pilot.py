#!/usr/bin/python
from Packages.Package import Package
from Packages.PackageType import PackageType
from Service import Service
from Manager import PlatformManager
from thread import *
import sys
from flask import Flask, request, make_response
import os

print(os.getpid())

manager = PlatformManager(timePerSession=1)
service = Service(sys.path[0] + '/config.yml', manager, True)
start_new_thread(service.run, ())

app = Flask(__name__)

@app.route("/")
def index():
	# set cookie
	token = request.args.get("stoken")
	if token != None and manager.isSessionValid(token):
		return "<p>" + "You are welcome! " + str(token) + "(" + str(manager.getCurSessionTime()) + ")" + "</p><!--<a href='http://localhost:5000/out?stoken=" + token + "'>Out</a>-->"
	return "<p>" + "You out. " + str(token) + "</p> "

'''
@app.route("/out")
def out():
	token = request.args.get("stoken")
	if manager.isSessionValid(token):
		manager.endSession()
		return "<p>Out</p><script>window.location.href='http://localhost:5000/'</script>"
	else:
		return "<p>Error</p>"

'''
app.run()
#p = Package("my value", PackageType.Token)
#print(p.getJSON())
