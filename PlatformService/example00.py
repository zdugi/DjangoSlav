#!/usr/bin/python
from Service import Service
from Manager import PlatformManager
from thread import *
import sys
from flask import Flask, request, make_response

manager = PlatformManager(timePerSession=1)
service = Service(sys.path[0] + '/config.yml', manager)
start_new_thread(service.run, ())

app = Flask(__name__)

@app.route("/")
def index():
	token = request.args.get("stoken")
	if token != None and manager.isSessionValid(token):
		return "<p>" + "You are welcome! " + str(token) + "(" + str(manager.getCurSessionTime()) + ")" + "</p>"
	return "<p>You out.</p> "


if __name__ == "__main__":
	app.run()