#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

import ctypes

# Abstracted from libmtp 0.3.3's libmtp.h. This must be kept in sync.
LIBMTP_Filetype = {
	"WAV":					ctypes.c_int(0),
	"MP3":					ctypes.c_int(1),
	"WMA":					ctypes.c_int(2),
	"OGG":					ctypes.c_int(3),
	"AUDIBLE":				ctypes.c_int(4),
	"MP4":					ctypes.c_int(5),
	"UNDEF_AUDIO":			ctypes.c_int(6),	
	"WMV":					ctypes.c_int(7),
	"AVI":					ctypes.c_int(8),
	"MPEG":					ctypes.c_int(9),
	"ASF":					ctypes.c_int(10),
	"QT":					ctypes.c_int(11),
	"UNDEF_VIDEO":			ctypes.c_int(12),
	"JPEG":					ctypes.c_int(13),
	"JFIF":					ctypes.c_int(14),
	"TIFF":					ctypes.c_int(15),
	"BMP":					ctypes.c_int(16),
	"GIF":					ctypes.c_int(17),
	"PICT":					ctypes.c_int(18),
	"PNG":					ctypes.c_int(19),
	"VCALENDAR1":			ctypes.c_int(20),
	"VCALENDAR2":			ctypes.c_int(21),
	"VCARD2":				ctypes.c_int(22),
	"VCARD3":				ctypes.c_int(23),
	"WINDOWSIMAGEFORMAT":	ctypes.c_int(24),
	"WINEXEC":				ctypes.c_int(25),
	"TEXT":					ctypes.c_int(26),
	"HTML":					ctypes.c_int(27),
	"FIRMWARE":				ctypes.c_int(28),
	"AAC":					ctypes.c_int(29),
	"MEDIACARD":			ctypes.c_int(30),
	"FLAC":					ctypes.c_int(31),
	"MP2":					ctypes.c_int(32),
	"M4A":					ctypes.c_int(33),
	"DOC":					ctypes.c_int(34),
	"XML":					ctypes.c_int(35),
	"XLS":					ctypes.c_int(36),
	"PPT":					ctypes.c_int(37),
	"MHT":					ctypes.c_int(38),
	"JP2":					ctypes.c_int(39),
	"JPX":					ctypes.c_int(40),
	"UNKNOWN":				ctypes.c_int(41),
	}
	
# Synced from libmtp 0.2.6.1's libmtp.h. Must be kept in sync.
LIBMTP_Error_Number = {
	"NONE":					ctypes.c_int(0),
	"GENERAL":				ctypes.c_int(1),
	"PTP_LAYER":			ctypes.c_int(2),
	"USB_LAYER":			ctypes.c_int(3),
	"MEMORY_ALLOCATION":	ctypes.c_int(4),
	"NO_DEVICE_ATTACHED":	ctypes.c_int(5),
	"STORAGE_FULL":			ctypes.c_int(6),
	"CONNECTING":			ctypes.c_int(7),
	"CANCELLED":			ctypes.c_int(8),
}
		