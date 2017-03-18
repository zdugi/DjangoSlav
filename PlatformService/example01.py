#!/usr/bin/python
from Service import Service
from Manager import PlatformManager
from thread import *
import sys
from flask import Flask, request, redirect

import time

# Platform communication config

CONFIG_FILE_PATH = sys.path[0] + '/config.yml' # full path

manager = PlatformManager()
service = Service(CONFIG_FILE_PATH, manager, debug=True)

start_new_thread(service.run, ()) # start platform communication service

# end

# now flask or whatever

def isUserLogin():
	global manager

	p = request.cookies.get('platform') #platform is cookie name
	
	return p != None and manager.isSessionValid(p)


app = Flask(__name__)

# setting token to cookie
@app.route("/")
def index():
	redirect_to_index = redirect('/home')
	response = app.make_response(redirect_to_index )

	token = request.args.get("stoken")

	if token != None and manager.isSessionValid(token):
		response.set_cookie('platform',value=token)

	return response

@app.route("/home")
def home():
	if isUserLogin():
		return "<p>Home</p><p>Your time: " + "(" + str(manager.getCurSessionTime()) + ")</p>"

	redirect_to_index = redirect('/error')
	response = app.make_response(redirect_to_index )
	return response

@app.route("/error")
def error():
	return "Ups!"

if __name__ == "__main__":
	app.run()