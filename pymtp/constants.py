#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

# Abstracted from libmtp 0.3.3's libmtp.h. This must be kept in sync.
LIBMTP_Filetype = dict(zip((
	"FOLDER",
	"WAV",
	"MP3",
	"WMA",
	"OGG",
	"AUDIBLE",
	"MP4",
	"UNDEF_AUDIO",
	"WMV",
	"AVI",
	"MPEG",
	"ASF",
	"QT",
	"UNDEF_VIDEO",
	"JPEG",
	"JFIF",
	"TIFF",
	"BMP",
	"GIF",
	"PICT",
	"PNG",
	"VCALENDAR1",
	"VCALENDAR2",
	"VCARD2",
	"VCARD3",
	"WINDOWSIMAGEFORMAT",
	"WINEXEC",
	"TEXT",
	"HTML",
	"FIRMWARE",
	"AAC",
	"MEDIACARD",
	"FLAC",
	"MP2",
	"M4A",
	"DOC",
	"XML",
	"XLS",
	"PPT",
	"MHT",
	"JP2",
	"JPX",
	"ALBUM",
	"PLAYLIST",
	"UNKNOWN",
	), range(99)))
LIBMTP_Filetype_reverse = dict([(LIBMTP_Filetype[n], n, ) for n in LIBMTP_Filetype])

# Synced from libmtp 0.2.6.1's libmtp.h. Must be kept in sync.
LIBMTP_Error_Number = dict(zip((
	"NONE",
	"GENERAL",
	"PTP_LAYER",
	"USB_LAYER",
	"MEMORY_ALLOCATION",
	"NO_DEVICE_ATTACHED",
	"STORAGE_FULL",
	"CONNECTING",
	"CANCELLED",
	), range(99)))
LIBMTP_Error_Number_reverse = dict([(LIBMTP_Error_Number[n], n, ) for n in LIBMTP_Error_Number])

class LIBMTP_STORAGE(object):
	SORTBY_NOTSORTED = 0
	SORTBY_FREESPACE = 1
	SORTBY_MAXSPACE = 2


class PTP_GOH(object):
	ALL_STORAGE = 0xffffffff
	ALL_FORMATS = 0x00000000
	ALL_ASSOCS = 0x00000000
	ROOT_PARENT = 0xffffffff
