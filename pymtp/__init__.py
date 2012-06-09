#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito <nick@nick125.com>
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

"""
	PyMTP is a pythonic wrapper around libmtp, making it a bit more
	friendly to be used in python

	Example Usage (or see examples/):
		>>> import pymtp
		>>> with = pymtp.MTP() as mtp:
		>>>     print mtp.get_devicename()
		>>>
"""

__VERSION_MACRO__ = 1
__VERSION_MINOR__ = 1
__VERSION_MAJOR__ = 0
__VERSION_TUPLE__ = (__VERSION_MAJOR__, __VERSION_MINOR__, __VERSION_MACRO__)
__VERSION__ = "{}.{}.{}".format(*__VERSION_TUPLE__)
__AUTHOR__ = "Nick Devito <nick@nick125.com>, M. Dietrich <mdt@pyneo.org>"
__LICENSE__ = "GPLv3"

from main import MTP
