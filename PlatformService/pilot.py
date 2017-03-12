#!/usr/bin/python
from Packages.Package import Package
from Packages.PackageType import PackageType
from Service import Service
from Manager import PlatformManager
from thread import *
import sys
from flask import Flask, request
import os

print(os.getpid())

manager = PlatformManager(timePerSession=20)
service = Service(sys.path[0] + '/config.yml', manager, True)
start_new_thread(service.run, ())

app = Flask(__name__)

@app.route("/")
def index():
	p = request.cookies.get('platform')
	if p != None and manager.isSessionValid(p):
		return "<p>" + "You are welcome! " + str(p) + "(" + str(manager.getCurSessionTime()) + ")" + "</p> <a href='http://localhost:5000/set'>Set</a><a href='http://localhost:5000/out'>Out</a>"
	return "<p>" + "You out. " + str(p) + "</p> <a href='http://localhost:5000/set'>Set</a>"

@app.route("/set")
def set():
	return "<script> var val = prompt('enter cookie'); document.cookie=\"platform=\" + val; window.location.href='http://localhost:5000/'</script>"

@app.route("/out")
def out():
	p = request.cookies.get('platform')
	if manager.isSessionValid(p):
		manager.endSession()
		return "<p>Out</p><script>window.location.href='http://localhost:5000/'</script>"
	else:
		return "<p>Error</p>"


app.run()
#p = Package("my value", PackageType.Token)
#print(p.getJSON())
