import socket
import sys
from thread import *
import time
import json
from Packages.Package import Package
from Packages.PackageType import PackageType
from thread import *
import hashlib

API_KEY = 'JQYB9KDR26CSPV5VnTJiOcsomOHZuhswo9s3dYkAyZaxh80p' # TOP SECRET!

HOST = ''

ADDRESS = '127.0.0.1'
PORT = 1337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

val = hashlib.sha224(str(time.time() * 100)).hexdigest()

print(sys.argv[0])

packageType = sys.argv[1]

data = None

if packageType == "token":
	print(val)
	data = Package({'value':val, 'time':time.time()}, PackageType.Token) # startTime, period
elif packageType == "info":
	data = Package({}, PackageType.Info)

try:
	s.bind((HOST, 0))
	s.connect((ADDRESS, PORT))

	#s.send(str.encode('Welcome, type your info\n'))
	s.sendall(data.getJSON())
	time.sleep(0.1)
	data = s.recv(1024)
	print(data)
	s.close()
except socket.error as e:
	print(str(e))
	s.close()
	exit()