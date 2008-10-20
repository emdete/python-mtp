#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

class NoDeviceConnected(Exception):
	"""
		Raised when there isn't a device connected to the USB bus
	"""

	pass

class AlreadyConnected(Exception):
	"""
		Raised when we're already connected to a device and there is
		an attempt to connect
	"""

	pass

class UnsupportedCommand(Exception):
	"""
		Raised when the connected device does not support the command
		issued
	"""

	pass

class CommandFailed(Exception):
	"""
		Raised when the connected device returned an error when trying
		to execute a command
	"""

	pass

class NotConnected(Exception):
	"""
		Raised when a command is called and the device is not connected
	"""

	pass

class ObjectNotFound(Exception):
	"""
		Raised when a command tries to get an object that doesn't exist
	"""

	pass