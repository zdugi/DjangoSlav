#!/usr/bin/python
import time, yaml, socket, sys
from thread import *
from Packages.Package import createPackage, Package
from Packages.PackageType import PackageType

KEY_LENGTH = 32
GLOBAL_KEY_LENGTH = 16
PACKAGE_SIZE = 1024

class Service:
	CHANNELS = 1

	def __init__(self, configFile, manager, debug = False):
		try:
			with open(configFile) as f:
				self.config = yaml.safe_load(f)

			self.address = self.config["app"]["host"]
			self.port = self.config["app"]["port"]
			self.key = self.config["app"]["key"][:KEY_LENGTH];
			self.iv = self.config["app"]["key"][0:GLOBAL_KEY_LENGTH];
		except Exception as e:
			self.print_d("[Service] Unable to load config file! (%s)" % (str(e)))
			exit()

		self.debug = debug
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.manager = manager

		self.statistic = dict()
		self.statistic["package"] = dict()
		self.statistic["package"]["valid"] = 0
		self.statistic["package"]["unvalid"] = 0

	def print_d(self, msg):
		if self.debug:
			tm = time.localtime(time.time())
			print(("[%02d:%02d:%02d] " % (tm.tm_hour, tm.tm_min, tm.tm_sec)) + msg)

	def __backProcess(self):
		if self.debug:
			self.print_d("Starting back process...")

		while True:
			self.manager.cistacica()
			time.sleep(10)

	def run(self):
		try:
			self.sock.bind((self.address, self.port))
		except socket.error as e:
			self.print_d("[Service] Error: " + str(e))
			exit()

		self.print_d("Service is started on %s:%d  [CTRL + C to exit]" % (self.address, self.port))

		self.sock.listen(self.CHANNELS)

		start_new_thread(self.__backProcess, ())

		try:
			while True:
				conn, addr = self.sock.accept()
				start_new_thread(self.__threaded_client, (conn,))
		except:
			self.sock.close()

	def __threaded_client(self, conn):
		while True:
			data = conn.recv(PACKAGE_SIZE)

			if not data:
				break

			#print(createPackage(data))
			self.manager.c.acquire()

			pack = createPackage(data)
			if pack != None:
				if pack["header"]["type"] == PackageType.Token:
					# maybe additional msg?!
					if self.manager.addSession(pack["value"]):
						p = Package(self.manager.statusJSON(),PackageType.Info)
						p.setMessage("successfully added")
						conn.sendall(p.getJSON())
					else:
						p = Package(self.manager.statusJSON(),PackageType.Warn)
						p.setMessage("unable to add")
						conn.sendall(p.getJSON())
				elif pack["header"]["type"] == PackageType.Info:
					if "value" in pack["value"]:
						self.manager.checkSession(pack["value"]["value"])
					p = Package(self.manager.statusJSON(),PackageType.Info)
					conn.sendall(p.getJSON())
			else:
				print(data)
				break
			self.manager.c.notify()
			self.manager.c.release()

		conn.close()