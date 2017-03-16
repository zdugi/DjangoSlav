#!/usr/bin/python
import time

class Red:
	def __init__(self):
		self.datas = list()

		self.curSessionStartTime = None

	def position(self, value):
		#with open("log2", "a") as f:
		#	f.write("\n[CKECK] value: " + value)
		#	f.write("\nList: " + str(self.datas))
		if value == '':
			return -1

		ind = -1

		for i in range(0, len(self.datas)):
			if value == self.datas[i]["value"]:
				ind = i
				break
		return ind

	def push(self, data):
		self.datas.append(data)

		# session time config
		if len(self.datas) == 1:
			self.setCur()

	def setCur(self):
		self.curSessionStartTime = time.time()

	def size(self):
		return len(self.datas)

	def getFirst(self):
		if self.size() == 0:
			return None
		return self.datas[0]

	def pop(self):
		if self.size() == 0:
			return None

		p = self.datas[0]
		del self.datas[0]

		# new session time config
		if len(self.datas) >= 1:
			self.setCur()
		else:
			self.curSessionStartTime = None

		return p