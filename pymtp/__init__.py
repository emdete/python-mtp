#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

"""
	PyMTP is a pythonic wrapper around libmtp, making it a bit more 
	friendly to use in python

	Example Usage (or see examples/):
		>>> import pymtp
		>>> mtp = pymtp.MTP()
	        >>> mtp.connect()
		PTP: Opening session
	        >>> print mtp.get_devicename()
	        Device name
	        >>> mtp.disconnect()
		PTP: Closing session
		>>>
"""

__VERSION__ = "0.1.0"
__VERSION_MACRO__ = 0
__VERSION_MINOR__ = 1
__VERSION_MAJOR__ = 0
__VERSION_TUPLE__ = (__VERSION_MAJOR__, __VERSION_MINOR__, __VERSION_MACRO__)
__AUTHOR__ = "Nick Devito (nick@nick125.com)"
__LICENSE__ = "GPL-3"

