#!/usr/bin/python
import threading
import json
import time
from Utils.Red import Red as Queue

class PlatformManager:
	def __init__(self, maxInQueue = None, timePerSession = 5):
		self.queue = Queue()

		self.timeBlock = timePerSession * 60 #timePerSession(mins) * 60s

		self.chSession = ""
		self.exp = None

		if maxInQueue == None:
			self.maxInQueue = 10
		else:
			self.maxInQueue = maxInQueue

		self.c = threading.Condition()

	#experimental
	def cistacica(self):
		self.c.acquire()

		x = self.queue.curSessionStartTime

		if x != None:
			t = time.time() - x

			num = int(t/self.timeBlock)

			for i in range(0, num):
				if num == self.maxInQueue:
					break
				self.queue.pop()

		self.c.notify()
		self.c.release()

	def addSession(self, tok):
		if self.queue.size() == self.maxInQueue:
			return False

		self.c.acquire()

		self.queue.push(tok)

		self.c.notify()
		self.c.release()

		return True

	def getCurSessionTime(self):
		if self.queue.curSessionStartTime != None:
			return (round(time.time() - self.queue.curSessionStartTime))
		else:
			return -1

	def calculateExp(self):
		self.exp = self.queue.size() * self.timeBlock

		p = self.getCurSessionTime()

		if p != -1:
			self.exp - p

	def isSessionValid(self, value):
		ind = False
		
		self.c.acquire()

		cur = self.queue.getFirst()
		if cur != None and cur["value"] == value:
			ind = True

		self.c.notify()
		self.c.release()

		return ind
	'''
	def endSession(self, value = None):
		return self.queue.pop()
	'''
	def checkSession(self, value):
		self.chSession = value

	def statusJSON(self):
		status = dict()

		status["position"] = self.queue.position(self.chSession)
		status["max"] = self.maxInQueue
		status["queue"] = self.queue.size()

		if self.exp != None:
			status["exp"] = self.exp
			self.exp = None

		return status