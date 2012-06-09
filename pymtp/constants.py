#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

from ctypes import c_int

# Abstracted from libmtp 0.3.3's libmtp.h. This must be kept in sync.
LIBMTP_Filetype = {
	"WAV":					c_int(0),
	"MP3":					c_int(1),
	"WMA":					c_int(2),
	"OGG":					c_int(3),
	"AUDIBLE":				c_int(4),
	"MP4":					c_int(5),
	"UNDEF_AUDIO":			c_int(6),
	"WMV":					c_int(7),
	"AVI":					c_int(8),
	"MPEG":					c_int(9),
	"ASF":					c_int(10),
	"QT":					c_int(11),
	"UNDEF_VIDEO":			c_int(12),
	"JPEG":					c_int(13),
	"JFIF":					c_int(14),
	"TIFF":					c_int(15),
	"BMP":					c_int(16),
	"GIF":					c_int(17),
	"PICT":					c_int(18),
	"PNG":					c_int(19),
	"VCALENDAR1":			c_int(20),
	"VCALENDAR2":			c_int(21),
	"VCARD2":				c_int(22),
	"VCARD3":				c_int(23),
	"WINDOWSIMAGEFORMAT":	c_int(24),
	"WINEXEC":				c_int(25),
	"TEXT":					c_int(26),
	"HTML":					c_int(27),
	"FIRMWARE":				c_int(28),
	"AAC":					c_int(29),
	"MEDIACARD":			c_int(30),
	"FLAC":					c_int(31),
	"MP2":					c_int(32),
	"M4A":					c_int(33),
	"DOC":					c_int(34),
	"XML":					c_int(35),
	"XLS":					c_int(36),
	"PPT":					c_int(37),
	"MHT":					c_int(38),
	"JP2":					c_int(39),
	"JPX":					c_int(40),
	"UNKNOWN":				c_int(41),
	}

# Synced from libmtp 0.2.6.1's libmtp.h. Must be kept in sync.
LIBMTP_Error_Number = {
	"NONE":					c_int(0),
	"GENERAL":				c_int(1),
	"PTP_LAYER":			c_int(2),
	"USB_LAYER":			c_int(3),
	"MEMORY_ALLOCATION":	c_int(4),
	"NO_DEVICE_ATTACHED":	c_int(5),
	"STORAGE_FULL":			c_int(6),
	"CONNECTING":			c_int(7),
	"CANCELLED":			c_int(8),
	}

