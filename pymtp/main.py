#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

from os import stat
from os.path import exists, isfile, basename
from ctypes.util import find_library
from ctypes import CDLL, c_int, c_void_p, byref, pointer, c_uint8, c_char_p, c_uint32
from models import *
from constants import *
from errors import *

_libmtp = CDLL(find_library("mtp"))

def libmtp_error_check(result, func, arguments):
	if result:
		MTP.debug_stack(arguments[0])
		raise CommandFailed(result)
	return result

# ----------
# Type Definitions
# Abstracted from libmtp 0.3.3's libmtp.h. This must be kept in sync.
# ----------

_libmtp.LIBMTP_Detect_Raw_Devices.argtypes = c_void_p, c_void_p,
_libmtp.LIBMTP_Detect_Raw_Devices.errcheck = libmtp_error_check
_libmtp.LIBMTP_Detect_Raw_Devices.restype = c_int
_libmtp.LIBMTP_Dump_Device_Info.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Dump_Device_Info.restype = None
# _libmtp.LIBMTP_Find_Folder.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Find_Folder.restype = LIBMTP_Folder_p
_libmtp.LIBMTP_Get_Batterylevel.argtypes = LIBMTP_MTPDevice_p, c_void_p, c_void_p,
_libmtp.LIBMTP_Get_Batterylevel.errcheck = libmtp_error_check
_libmtp.LIBMTP_Get_Batterylevel.restype = c_int
_libmtp.LIBMTP_Get_Deviceversion.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Deviceversion.restype = c_char_p
# _libmtp.LIBMTP_Get_Errorstack.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Errorstack.restype = LIBMTP_Error_p
_libmtp.LIBMTP_Get_Filelisting_With_Callback.argtypes = LIBMTP_MTPDevice_p, c_void_p, c_void_p,
_libmtp.LIBMTP_Get_Filelisting_With_Callback.restype = LIBMTP_File_p
_libmtp.LIBMTP_Get_Filemetadata.argtypes = LIBMTP_MTPDevice_p, c_int
_libmtp.LIBMTP_Get_Filemetadata.restype = LIBMTP_File_p
# _libmtp.LIBMTP_Get_Filetype_Description.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Filetype_Description.restype = c_char_p
_libmtp.LIBMTP_Get_First_Device.argtypes = tuple()
_libmtp.LIBMTP_Get_First_Device.restype = LIBMTP_MTPDevice_p
# _libmtp.LIBMTP_Get_Folder_List.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Folder_List.restype = LIBMTP_Folder_p
_libmtp.LIBMTP_Get_Friendlyname.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Friendlyname.restype = c_char_p
_libmtp.LIBMTP_Get_Manufacturername.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Manufacturername.restype = c_char_p
_libmtp.LIBMTP_Get_Modelname.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Modelname.restype = c_char_p
# _libmtp.LIBMTP_Get_Playlist.argtypes = LIBMTP_MTPDevice_p,
# _libmtp.LIBMTP_Get_Playlist_List.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Playlist_List.restype = LIBMTP_Playlist_p
_libmtp.LIBMTP_Get_Playlist.restype = LIBMTP_Playlist_p
_libmtp.LIBMTP_Get_Serialnumber.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Serialnumber.restype = c_char_p
_libmtp.LIBMTP_Get_Storage.argtypes = LIBMTP_MTPDevice_p, c_int,
_libmtp.LIBMTP_Get_Storage.errcheck = libmtp_error_check
_libmtp.LIBMTP_Get_Storage.restype = c_int
# _libmtp.LIBMTP_Get_Tracklisting_With_Callback.argtypes = LIBMTP_MTPDevice_p, c_void_p, c_void_p,
_libmtp.LIBMTP_Get_Tracklisting_With_Callback.restype = LIBMTP_Track_p
# _libmtp.LIBMTP_Get_Trackmetadata.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Trackmetadata.restype = LIBMTP_Track_p
_libmtp.LIBMTP_Get_Track_To_File.argtypes = LIBMTP_MTPDevice_p, c_uint32, c_char_p, Progressfunc, c_void_p,
_libmtp.LIBMTP_Get_Track_To_File.errcheck = libmtp_error_check
_libmtp.LIBMTP_Get_Track_To_File.restype = c_int
_libmtp.LIBMTP_Init.argtypes = tuple()
_libmtp.LIBMTP_Init.restype = None
_libmtp.LIBMTP_Open_Raw_Device_Uncached.argtypes = LIBMTP_RawDevice_p,
_libmtp.LIBMTP_Open_Raw_Device_Uncached.restype = LIBMTP_MTPDevice_p
_libmtp.LIBMTP_Reset_Device.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Reset_Device.errcheck = libmtp_error_check
_libmtp.LIBMTP_Reset_Device.restype = c_int
_libmtp.LIBMTP_Send_File_From_File.argtypes = LIBMTP_MTPDevice_p, c_char_p, LIBMTP_File_p, Progressfunc, c_void_p,
_libmtp.LIBMTP_Send_File_From_File.errcheck = libmtp_error_check
_libmtp.LIBMTP_Send_File_From_File.restype = c_int
_libmtp.LIBMTP_Set_Debug.argtypes = c_int,
_libmtp.LIBMTP_Set_Debug.restype = None
_libmtp.LIBMTP_Set_Friendlyname.argtypes = LIBMTP_MTPDevice_p, c_char_p
_libmtp.LIBMTP_Set_Friendlyname.errcheck = libmtp_error_check
_libmtp.LIBMTP_Set_Friendlyname.restype = c_int
_libmtp.LIBMTP_Send_Track_From_File.argtypes = LIBMTP_MTPDevice_p, c_char_p, LIBMTP_Track_p, Progressfunc, c_void_p,
_libmtp.LIBMTP_Send_Track_From_File.errcheck = libmtp_error_check
_libmtp.LIBMTP_Send_Track_From_File.restype = c_int

# Initialize LibMTP here to make sure that it only gets initialized once
_libmtp.LIBMTP_Init()

# ----------
# End Type Definitions
# ----------

class MTP(object):
	"""
		The MTP object
		This is the main wrapper around libmtp
	"""

	@staticmethod
	def detect_rawdevices():
		"""
			Detects the MTP devices on the USB bus that we can connect to

			@rtype: L{MTPRawDevices}
			@return: An array/list of L{MTPRawDevice} objects
		"""
		numdevices = c_int(0)
		devices = LIBMTP_RawDevice_p()
		_libmtp.LIBMTP_Detect_Raw_Devices(byref(devices), byref(numdevices))
		return [devices[n] for n in range(numdevices.value)]

	def __init__(self, cached=True, ):
		"""
			Initializes the MTP object

			@rtype: None
			@return: None
		"""
		self.device = None
		self.cached = cached

	def __enter__(self):
		"""
			Initializes the MTP connection to the device

			@rtype: None
			@return: None

		"""
		if self.device:
			raise AlreadyConnected()
		if self.cached:
			self.device = _libmtp.LIBMTP_Get_First_Device()
		else:
			rawdevices = self.detect_rawdevices()
			self.device = _libmtp.LIBMTP_Open_Raw_Device_Uncached(rawdevices[0])
		if not self.device:
			self.device = None
			raise NoDeviceFound()
		_libmtp.LIBMTP_Clear_Errorstack(self.device)
		#_libmtp.LIBMTP_Reset_Device(self.device)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		"""
			Disconnects the MTP device and deletes the self.device object

			@rtype: None
			@return: None
		"""
		if exc_value:
			self.debug_stack(self.device)
		if self.device:
			_libmtp.LIBMTP_Release_Device(self.device)
		self.device = None

	@staticmethod
	def set_debug(debug):
		_libmtp.LIBMTP_Set_Debug(debug);

	@staticmethod
	def debug_stack(device):
		"""
			dumps and clears the errorstack.

			@rtype: None
			@return: None
		"""
		_libmtp.LIBMTP_Dump_Errorstack(device)
		_libmtp.LIBMTP_Clear_Errorstack(device)

	def dump_info(self):
		_libmtp.LIBMTP_Dump_Device_Info(self.device)

	def get_devicename(self):
		"""
			Returns the connected device's 'friendly name' (or
			known as the owner name)

			@rtype: string
			@return: The connected device's 'friendly name'
		"""
		if not self.device:
			raise NotConnected()
		return _libmtp.LIBMTP_Get_Friendlyname(self.device)

	def set_devicename(self, name):
		"""
			Changes the connected device's 'friendly name' to name

			@type name: string
			@param name: The name to change the connected device's 'friendly name' to
			@rtype: None
			@return: None
		"""
		if not self.device:
			raise NotConnected()
		_libmtp.LIBMTP_Set_Friendlyname(self.device, name)

	def get_serialnumber(self):
		"""
			Returns the connected device's serial number

			@rtype: string
			@return: The connected device's serial number
		"""
		if not self.device:
			raise NotConnected()
		return _libmtp.LIBMTP_Get_Serialnumber(self.device)

	def get_manufacturer(self):
		"""
			Return the connected device's manufacturer

			@rtype: string
			@return: The connected device's manufacturer
		"""
		if not self.device:
			raise NotConnected()
		return _libmtp.LIBMTP_Get_Manufacturername(self.device)

	def get_batterylevel(self):
		"""
			Returns the connected device's maximum and current
			battery levels

			@rtype: tuple
			@return: The connected device's maximum and current battery levels ([0] is maximum, [1] is current)
		"""
		if not self.device:
			raise NotConnected()
		maximum_level = c_uint8()
		current_level = c_uint8()
		ret = _libmtp.LIBMTP_Get_Batterylevel(self.device, byref(maximum_level), byref(current_level))
		return (maximum_level.value, current_level.value)

	def get_modelname(self):
		"""
			Returns the connected device's model name (such
			as "Zen V Plus")

			@rtype: string
			@return: The connected device's model name
		"""
		if not self.device:
			raise NotConnected()
		return _libmtp.LIBMTP_Get_Modelname(self.device)

	def get_deviceversion(self):
		"""
			Returns the connected device's version (such as
			firmware/hardware version)

			@rtype: string
			@return: Returns the connect device's version information
		"""
		if not self.device:
			raise NotConnected
		return _libmtp.LIBMTP_Get_Deviceversion(self.device)

	def get_filelisting(self, callback=None):
		"""
			Returns the connected device's file listing as a tuple,
			containing L{LIBMTP_File} objects.

			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback must take two arguments, total and sent (in bytes)
			@rtype: tuple
			@return: Returns the connect device file listing tuple
		"""
		if not self.device:
			raise NotConnected()
		if callback:
			callback = Progressfunc(callback)
		files = _libmtp.LIBMTP_Get_Filelisting_With_Callback(self.device, callback, None)
		ret = []
		next = files
		while next:
			ret.append(next.contents)
			if not next.contents.next:
				break
			next = next.contents.next
		return ret

	def get_filetype_description(self, filetype):
		"""
			Returns the description of the filetype

			@type filetype: int
			@param filetype: The MTP filetype integer
			@rtype: string
			@return: The file type information
		"""
		if not self.device:
			raise NotConnected()
		return _libmtp.LIBMTP_Get_Filetype_Description(filetype)

	def get_file_metadata(self, file_id):
		"""
			Returns the file metadata from the connected device

			As per the libmtp documentation, calling this function
			repeatly is not recommended, as it is slow and creates
			a large amount of USB traffic.

			@type file_id: int
			@param file_id: The unique numeric file id
			@rtype: LIBMTP_File
			@return: The file metadata
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Filemetadata(self.device, file_id)
		if not hasattr(ret, 'contents'):
			raise ObjectNotFound()
		return ret.contents

	def get_tracklisting(self, callback=None):
		"""
			Returns tracks from the connected device

			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback must take two arguments, total and sent (in bytes)
			@rtype: tuple
			@return: Returns a tuple full of L{LIBMTP_Track} objects
		"""
		if not self.device:
			raise NotConnected()
		if callback:
			callback = Progressfunc(callback)
		tracks = _libmtp.LIBMTP_Get_Tracklisting_With_Callback(self.device, callback, None)
		ret = []
		next = tracks
		while next:
			ret.append(next.contents)
			if not next.contents.next:
				break
			next = next.contents.next
		return ret

	def get_track_metadata(self, track_id):
		"""
			Returns the track metadata

			As per the libmtp documentation, calling this function repeatly is not
			recommended, as it is slow and creates a large amount of USB traffic.

			@type track_id: int
			@param track_id: The unique numeric track id
			@rtype: L{LIBMTP_Track}
			@return: The track metadata
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Trackmetadata(self.device, track_id)
		if not hasattr(ret, 'contents'):
			raise ObjectNotFound()
		return ret.contents

	def get_file_to_file(self, file_id, target, callback=None):
		"""
			Downloads the file from the connected device and stores it at the
			target location

			@type file_id: int
			@param file_id: The unique numeric file id
			@type target: str
			@param target: The location to place the file
			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback must take two arguments, total and sent (in bytes)
		"""
		if not self.device:
			raise NotConnected()
		if callback:
			callback = Progressfunc(callback)
		ret = _libmtp.LIBMTP_Get_File_To_File(self.device, file_id, target, callback, None)
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)

	def get_track_to_file(self, track_id, target, callback=None):
		"""
			Downloads the track from the connected device and stores it at
			the target location

			@type track_id: int
			@param track_id: The unique numeric track id
			@type target: str
			@param target: The location to place the track
			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback must take two arguments, total and sent (in bytes)
		"""
		if not self.device:
			raise NotConnected()
		if callback:
			callback = Progressfunc(callback)
		_libmtp.LIBMTP_Get_Track_To_File(self.device, track_id, target, callback, None)

	def find_filetype(self, filename):
		"""
			Attempts to guess the filetype off the filename. Kind of
			inaccurate and should be trusted with a grain of salt. It
			works in most situations, though.

			@type filename: str
			@param filename: The filename to attempt to guess from
			@rtype: int
			@return: The integer of the Filetype
		"""
		fileext = filename.split(".")[-1].lower()
		if fileext == "wav" or fileext == "wave":
			return LIBMTP_Filetype["WAV"]
		elif fileext == "mp3":
			return LIBMTP_Filetype["MP3"]
		elif fileext == "wma":
			return LIBMTP_Filetype["WMA"]
		elif fileext == "ogg":
			return LIBMTP_Filetype["OGG"]
		elif fileext == "mp4":
			return LIBMTP_Filetype["MP4"]
		elif fileext == "wmv":
			return LIBMTP_Filetype["WMV"]
		elif fileext == "avi":
			return LIBMTP_Filetype["AVI"]
		elif fileext == "mpeg" or fileext == "mpg":
			return LIBMTP_Filetype["MPEG"]
		elif fileext == "asf":
			return LIBMTP_Filetype["ASF"]
		elif fileext == "qt" or fileext == "mov":
			return LIBMTP_Filetype["QT"]
		elif fileext == "jpeg" or fileext == "jpg":
			return LIBMTP_Filetype["JPEG"]
		elif fileext == "jfif":
			return LIBMTP_Filetype["JFIF"]
		elif fileext == "tif" or fileext == "tiff":
			return LIBMTP_Filetype["TIFF"]
		elif fileext == "bmp":
			return LIBMTP_Filetype["BMP"]
		elif fileext == "gif":
			return LIBMTP_Filetype["GIF"]
		elif fileext == "pic" or fileext == "pict":
			return LIBMTP_Filetype["PICT"]
		elif fileext == "png":
			return LIBMTP_Filetype["PNG"]
		elif fileext == "wmf":
			return LIBMTP_Filetype["WINDOWSIMAGEFORMAT"]
		elif fileext == "ics":
			return LIBMTP_Filetype["VCALENDAR2"]
		elif fileext == "exe" or fileext == "com" or fileext == "bat" or fileext == "dll" or fileext == "sys":
			return LIBMTP_Filetype["WINEXEC"]
		elif fileext == "aac":
			return LIBMTP_Filetype["AAC"]
		elif fileext == "mp2":
			return LIBMTP_Filetype["MP2"]
		elif fileext == "flac":
			return LIBMTP_Filetype["FLAC"]
		elif fileext == "m4a":
			return LIBMTP_Filetype["M4A"]
		elif fileext == "doc":
			return LIBMTP_Filetype["DOC"]
		elif fileext == "xml":
			return LIBMTP_Filetype["XML"]
		elif fileext == "xls":
			return LIBMTP_Filetype["XLS"]
		elif fileext == "ppt":
			return LIBMTP_Filetype["PPT"]
		elif fileext == "mht":
			return LIBMTP_Filetype["MHT"]
		elif fileext == "jp2":
			return LIBMTP_Filetype["JP2"]
		elif fileext == "jpx":
			return LIBMTP_Filetype["JPX"]
		else:
			return LIBMTP_Filetype["UNKNOWN"]

	def send_file_from_file(self, source, target, parent=0, callback=None):
		"""
			Sends a file from the filesystem to the connected device
			and stores it at the target filename inside the parent.

			This will attempt to "guess" the filetype with
			find_filetype()

			@type source: str
			@param source: The path on the filesystem where the file resides
			@type target: str
			@param target: The target filename on the device
			@type parent: int or 0
			@param parent: The parent directory for the file to go into; If 0, the file goes into main directory
			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback function must take two arguments, sent and total (in bytes)
			@rtype: int
			@return: The object ID of the new file
		"""
		if not self.device:
			raise NotConnected()
		if not isfile(source):
			raise IOError()
		if callback:
			callback = Progressfunc(callback)
		metadata = LIBMTP_File(filename=target, filetype=self.find_filetype(source), filesize=stat(source).st_size)
		_libmtp.LIBMTP_Send_File_From_File(self.device, source, pointer(metadata), callback, None, parent)
		return metadata.item_id

	def send_track_from_file(self, source, tags, parent=0, callback=None, data=None):
		"""
			Sends a track from the filesystem to the connected
			device

			@type source: str
			@param source: The path where the track resides
			@type target: str
			@param target: The target filename on the device
			@type metadata: LIBMTP_Track
			@param metadata: The track metadata
			@type parent: int or 0
			@param parent: The parent directory for the track; if 0, the track will be placed in the base dir.
			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback function must take two arguments, sent and total (in bytes)
			@rtype: int
			@return: The object ID of the new track
		"""
		if not self.device:
			raise NotConnected()
		if not exists(source):
			raise IOError()
		if callback:
			callback = Progressfunc(callback)
		metadata = LIBMTP_Track()
		if 'ARTIST' in tags:
			metadata.artist = tags['ARTIST']
		if 'TITLE' in tags:
			metadata.title = tags['TITLE']
		if 'ALBUM' in tags:
			metadata.album = tags['ALBUM']
		if 'TRACKNUMBER' in tags:
			metadata.tracknumber = int(tags['TRACKNUMBER'])
		metadata.filename = basename(source)
		metadata.parent_id = parent
		metadata.storage_id = 0
		metadata.filetype = self.find_filetype(source)
		metadata.filesize = stat(source).st_size
		_libmtp.LIBMTP_Send_Track_From_File(self.device, source, metadata, callback, data)
		return metadata

	def get_freespace(self):
		"""
			Returns the amount of free space on the connected device
			@rtype: long
			@return: The amount of free storage in bytes
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE.SORTBY_NOTSORTED)
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)
		if not self.device.contents.storage:
			raise AssertionError('no storage')
		return self.device.contents.storage.contents.FreeSpaceInBytes

	def get_totalspace(self):
		"""
			Returns the total space on the connected device
			@rtype: long
			@return: The amount of total storage in bytes
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE.SORTBY_NOTSORTED)
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)
		if not self.device.contents.storage:
			raise AssertionError('no storage')
		return self.device.contents.storage.contents.MaxCapacity

	def get_usedspace(self):
		"""
			Returns the amount of used space on the connected device

			@rtype: long
			@return: The amount of used storage in bytes
		"""

		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE.SORTBY_NOTSORTED)
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)
		if not self.device.contents.storage:
			raise AssertionError('no storage')
		storage = self.device.contents.storage.contents
		return (storage.MaxCapacity - storage.FreeSpaceInBytes)

	def get_usedspace_percent(self):
		"""
			Returns the amount of used space as a percentage

			@rtype: float
			@return: The percentage of used storage
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE.SORTBY_NOTSORTED)
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)
		if not self.device.contents.storage:
			raise AssertionError('no storage')
		storage = self.device.contents.storage.contents
		# Why don't we call self.get_totalspace/self.get_usedspace
		# here? That would require 3 *more* calls to
		# LIBMTP_Get_Storage
		usedspace = storage.MaxCapacity - storage.FreeSpaceInBytes
		return ((float(usedspace) / float(storage.MaxCapacity)) * 100)

	def delete_object(self, object_id):
		"""
			Deletes the object off the connected device.

			@type object_id: int
			@param object_id: The unique object identifier
		"""

		if not self.device:
			raise NotConnected
		ret = _libmtp.LIBMTP_Delete_Object(self.device, object_id)
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)

	def get_playlists(self):
		"""
			Returns a tuple filled with L{LIBMTP_Playlist} objects
			from the connected device.

			The main gotcha of this function is that the tracks
			variable of LIBMTP_Playlist isn't iterable (without
			segfaults), so, you have to iterate over the no_tracks
			(through range or xrange) and access it that way (i.e.
			tracks[track_id]). Kind of sucks.

			@rtype: tuple
			@return: Tuple filled with LIBMTP_Playlist objects
		"""
		if not self.device:
			raise NotConnected()
		playlists = _libmtp.LIBMTP_Get_Playlist_List(self.device)
		ret = []
		next = playlists

		while next:
			ret.append(next.contents)
			if not next.contents.next:
				break
			next = next.contents.next

		return ret

	def get_playlist(self, playlist_id):
		"""
			Returns a L{LIBMTP_Playlist} object of the requested
			playlist_id from the connected device

			@type playlist_id: int
			@param playlist_id: The unique playlist identifier
			@rtype: LIBMTP_Playlist
			@return: The playlist object
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Playlist(self.device, playlist_id).contents
		if ret != 0:
			self.debug_stack(self.device)
			raise ObjectNotFound()
		return ret

	def create_new_playlist(self, metadata, parent=0):
		"""
			Creates a new playlist based on the metadata object
			passed.

			@type metadata: LIBMTP_Playlist
			@param metadata: A LIBMTP_Playlist object describing the playlist
			@type parent: int or 0
			@param parent: The parent ID or 0 for base
			@rtype: int
			@return: The object ID of the new playlist
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Create_New_Playlist(self.device, pointer(metadata), parent)
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)
		return ret

	def update_playlist(self, metadata):
		"""
			Updates a playlist based on the supplied metadata.

			When updating the tracks field in a playlist, this
			function will replace the playlist's tracks with
			the tracks supplied in the metadata object. This
			means that the previous tracks in the playlist
			will be overwritten.

			@type metadata: LIBMTP_Playlist
			@param metadata: A LIBMTP_Playlist object describing the updates to the playlist.
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Update_Playlist(self.device, pointer(metadata))
		if ret != 0:
			self.debug_stack(self.device)
			raise CommandFailed(ret)

	def get_folder_list(self):
		"""
			Returns a pythonic dict of the folders on the
			device.

			@rtype: dict
			@return: A dict of the folders on the device where the folder ID is the key.
		"""
		if not self.device:
			raise NotConnected()
		folders = _libmtp.LIBMTP_Get_Folder_List(self.device)
		next = folders
		# List of folders, key being the folder ID
		ret = {}
		# Iterate over the folders to grab the first-level parents
		while True:
			next = next.contents
			scanned = True
			# Check if this ID exists, if not, add it
			# and trigger a scan of the children
			if not (ret.has_key(next.folder_id)):
				ret[next.folder_id] = next
				scanned = False
			if not scanned and next.child:
				## Scan the children
				next = next.child
			elif next.sibling:
				## Scan the siblings
				next = next.sibling
			elif next.parent_id != 0:
				## If we have no children/siblings to visit,
				## and we aren't at the parent, go back to
				## the parent.
				next = _libmtp.LIBMTP_Find_Folder(folders, int(next.parent_id))
			else:
				## We have scanned everything, let's go home.
				break
		return ret

	def get_parent_folders(self):
		"""
			Returns a list of only the parent folders.
			@rtype: list
			@return: Returns a list of the parent folders
		"""

		if not self.device:
			raise NotConnected()
		folders = _libmtp.LIBMTP_Get_Folder_List(self.device)
		next = folders
		# A temporary holding space, this makes checking folder
		# IDs easier
		tmp = {}
		while True:
			next = next.contents
			## Check if this folder is in the dict
			if not (tmp.has_key(next.folder_id)):
				tmp[next.folder_id] = next
			# Check for siblings
			if next.sibling:
				## Scan the sibling
				next = next.sibling
			else:
				## We're done here.
				break

		## convert the dict into a list
		ret = []
		for key in tmp:
			ret.append(tmp[key])
		return ret

	def create_folder(self, name, parent=0):
		"""
			This creates a new folder in the parent. If the parent
			is 0, it will go in the main directory.

			@type name: str
			@param name: The name for the folder
			@type parent: int
			@param parent: The parent ID or 0 for main directory
			@rtype: int
			@return: Returns the object ID of the new folder
		"""
		if not self.device:
			raise NotConnected()
		_libmtp.LIBMTP_Create_Folder(self.device, name, parent)
		return ret

	def get_errorstack(self):
		"""
			Returns the connected device's errorstack from
			LIBMTP.
			@rtype: L{LIBMTP_Error}
			@return: An array of LIBMTP_Errors.
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Errorstack(self.device)
		return ret

