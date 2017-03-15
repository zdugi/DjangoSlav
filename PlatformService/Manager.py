#!/usr/bin/python
import threading
import json
import time
from Utils.Red import Red as Queue

class PlatformManager:
	def __init__(self, maxInQueue = None, timePerSession = None):
		self.queue = Queue()

		self.timeBlock = timePerSession * 60#timePerSession 5 * 60s

		self.chSession = ""

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

			#print("[CISTATICA] sad brisem: " + str(num))

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

		# value, start, period
		# add session
		self.queue.push(tok)

		self.c.notify()
		self.c.release()

		return True

	def getCurSessionTime(self):
		if self.queue.curSessionStartTime != None:
			return (round(time.time() - self.queue.curSessionStartTime))
		else:
			return -1

	def isSessionValid(self, value):
		#self.cistacica()

		ind = False
		
		self.c.acquire()

		cur = self.queue.getFirst()
		if cur != None and cur["value"] == value:
			ind = True

		self.c.notify()
		self.c.release()

		return ind

	def endSession(self, value = None):
		return self.queue.pop()

	def checkSession(self, value):
		self.chSession = value

	def statusJSON(self):
		status = dict()
		status["position"] = self.queue.position(self.chSession)
		status["max"] = self.maxInQueue
		status["queue"] = self.queue.size()

		return status