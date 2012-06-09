#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

class NoDeviceFound(Exception):
	"""
		Raised when there wasn't a device found
	"""

class AlreadyConnected(Exception):
	"""
		Raised when we're already connected to a device and there is
		an attempt to connect
	"""

class UnsupportedCommand(Exception):
	"""
		Raised when the connected device does not support the command
		issued
	"""

class CommandFailed(Exception):
	"""
		Raised when the connected device returned an error when trying
		to execute a command
	"""

class NotConnected(Exception):
	"""
		Raised when a command is called and the device is not connected
	"""

class ObjectNotFound(Exception):
	"""
		Raised when a command tries to get an object that doesn't exist
	"""
