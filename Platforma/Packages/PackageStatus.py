#!/usr/bin/python
from enum import Enum

class PackageStatus(Enum):
	OK = 1
	ERROR = 2
	FATAL_ERROR = 3