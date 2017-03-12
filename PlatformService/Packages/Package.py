#!/usr/bin/python
import json
import hashlib
from enum import IntEnum
from PackageStatus import PackageStatus
from PackageType import PackageType
from uuid import getnode as get_mac


def createPackage(jsonString):
	try:
		#should chack package more
		package = json.loads(jsonString)

		package["header"]["type"] = PackageType(package["header"]["type"])
		package["header"]["status"] = PackageStatus(package["header"]["status"])
		
		return package
	except Exception as e:
		print('[TOOL] Unable to extract package from json.(%s)' % (str(e)))
		return None

class Package:
	SIZE = 1024

	def __init__(self, value, packageType, status = None):
		self.setValue(value)
		self.packageType = packageType
		self.size = self.SIZE
		self.msg = None

		if status == None: 
			self.status = PackageStatus.OK 
		else:
			self.status = status

		self.senderMac = get_mac()

	def setValue(self, value):
		string = value
		if type(value) is dict:
			string = json.dumps(value)

		self.__value = value
		self.__hashsum = hashlib.sha224(string).hexdigest()


	def setStatus(self, status):
		self.status = status

	def setMessage(self, msg):
		self.msg = msg

	def getJSON(self):
		package = dict()

		package["header"] = dict()
		package["header"]["status"] = self.status.value
		package["header"]["type"] = self.packageType.value
		package["header"]["hashsum"] = self.__hashsum
		package["header"]["sender"] = self.senderMac

		if self.msg != None:
			package["header"]["message"] = self.msg

		package["value"] = self.__value

		jsonString = json.dumps(package)

		if len(jsonString) > self.SIZE:
			print('[PACKAGE] Package is too large, %dB (%dB allowed)' % (len(jsonString), self.SIZE))

			return None

		return jsonString