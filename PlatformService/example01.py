#!/usr/bin/python
from Service import Service
from Manager import PlatformManager
from thread import *
import sys
from flask import Flask, request

import time

# test
import os
print("Pid: " + str(os.getpid()))
#test

# Platform communication config

CONFIG_FILE_PATH = sys.path[0] + '/config.yml' # full path

manager = PlatformManager()
service = Service(CONFIG_FILE_PATH, manager)

start_new_thread(service.run, ()) # start platform communication service

# end

# now flask or whatever

def isUserLogin():
	global manager

	p = request.cookies.get('platform') #platform is cookie name
	
	return p != None and manager.isSessionValid(p)


app = Flask(__name__)

@app.route("/home")
def home():
	return "Home"

@app.route("/")
def index():
	if isUserLogin():
		return "<p>You are login!</p><br><p>Login time: " + str(manager.getCurSessionTime()) + "</p>" + "<a href='http://localhost:5000/out'>Logout</a>"
	return "<p>" + "You are not login!</p> <a href='http://localhost:5000/set'>Login now</a>"

@app.route("/set")
def set():
	if not isUserLogin():
		return "<script> var val = prompt('enter cookie'); document.cookie=\"platform=\" + val; window.location.href='http://localhost:5000/'</script>"
	return "Wrong request!"

@app.route("/out")
def out():
	if isUserLogin():
		manager.endSession()
		return "<p>Out</p><script>window.location.href='http://localhost:5000/'</script>"
	return "<p>Error</p>"

if __name__ == "__main__":
	app.run()
