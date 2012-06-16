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
from datetime import datetime
from ctypes.util import find_library
from ctypes import CDLL, c_int, c_void_p, byref, pointer, c_uint8, c_char_p, c_uint32
from models import *
from constants import *
from errors import *

_libmtp = CDLL(find_library("mtp"))

def libmtp_check_null(result, func, arguments):
	if not result:
		raise ObjectNotFound(func.__name__)
	return result

def libmtp_check_return(result, func, arguments):
	if result:
		MTP.debug_stack(arguments[0])
		raise CommandFailed(func.__name__, result)
	return result

# ----------
# Type Definitions
# Abstracted from libmtp 0.3.3's libmtp.h. This must be kept in sync.
# ----------
_libmtp.LIBMTP_Clear_Errorstack.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Clear_Errorstack.restype = None
_libmtp.LIBMTP_Create_Folder.argtypes = LIBMTP_MTPDevice_p, c_char_p, c_uint32, c_uint32,
_libmtp.LIBMTP_Create_Folder.errcheck = libmtp_check_return
_libmtp.LIBMTP_Create_Folder.restype = c_int
_libmtp.LIBMTP_Create_New_Playlist.argtypes = LIBMTP_MTPDevice_p, LIBMTP_Playlist_p, c_uint32
_libmtp.LIBMTP_Create_New_Playlist.errcheck = libmtp_check_return
_libmtp.LIBMTP_Create_New_Playlist.restype = c_int
_libmtp.LIBMTP_Delete_Object.argtypes = LIBMTP_MTPDevice_p, c_uint32
_libmtp.LIBMTP_Delete_Object.errcheck = libmtp_check_return
_libmtp.LIBMTP_Delete_Object.restype = c_int
_libmtp.LIBMTP_destroy_file_t.argtypes = LIBMTP_File_p,
_libmtp.LIBMTP_destroy_file_t.restype = None
_libmtp.LIBMTP_destroy_folder_t.argtypes = LIBMTP_Folder_p,
_libmtp.LIBMTP_destroy_folder_t.restype = None
_libmtp.LIBMTP_destroy_playlist_t.argtypes = LIBMTP_Playlist_p,
_libmtp.LIBMTP_destroy_playlist_t.restype = None
_libmtp.LIBMTP_destroy_track_t.argtypes = LIBMTP_Track_p,
_libmtp.LIBMTP_destroy_track_t.restype = None
_libmtp.LIBMTP_Detect_Raw_Devices.argtypes = c_void_p, c_void_p,
# _libmtp.LIBMTP_Detect_Raw_Devices.errcheck = libmtp_check_return
_libmtp.LIBMTP_Detect_Raw_Devices.restype = c_int
_libmtp.LIBMTP_Dump_Device_Info.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Dump_Device_Info.restype = None
_libmtp.LIBMTP_Dump_Errorstack.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Dump_Errorstack.restype = None
_libmtp.LIBMTP_Get_Batterylevel.argtypes = LIBMTP_MTPDevice_p, c_void_p, c_void_p,
_libmtp.LIBMTP_Get_Batterylevel.errcheck = libmtp_check_return
_libmtp.LIBMTP_Get_Batterylevel.restype = c_int
_libmtp.LIBMTP_Get_Deviceversion.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Deviceversion.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Deviceversion.restype = c_char_p
_libmtp.LIBMTP_Get_Errorstack.argtypes = LIBMTP_MTPDevice_p,
# _libmtp.LIBMTP_Get_Errorstack.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Errorstack.restype = LIBMTP_Error_p
_libmtp.LIBMTP_Get_Filelisting_With_Callback.argtypes = LIBMTP_MTPDevice_p, Progressfunc, c_void_p,
_libmtp.LIBMTP_Get_Filelisting_With_Callback.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Filelisting_With_Callback.restype = LIBMTP_File_p
_libmtp.LIBMTP_Get_Filemetadata.argtypes = LIBMTP_MTPDevice_p, c_int
_libmtp.LIBMTP_Get_Filemetadata.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Filemetadata.restype = LIBMTP_File_p
_libmtp.LIBMTP_Get_Files_And_Folders.argtypes = LIBMTP_MTPDevice_p, c_uint32, c_uint32,
_libmtp.LIBMTP_Get_Files_And_Folders.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Files_And_Folders.restype = LIBMTP_File_p
_libmtp.LIBMTP_Get_File_To_File.argtypes = LIBMTP_MTPDevice_p, c_uint32, c_char_p, Progressfunc, c_void_p
_libmtp.LIBMTP_Get_File_To_File.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_File_To_File.restype = c_int
_libmtp.LIBMTP_Get_Filetype_Description.argtypes = LIBMTP_File_p,
_libmtp.LIBMTP_Get_Filetype_Description.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Filetype_Description.restype = c_char_p
_libmtp.LIBMTP_Get_First_Device.argtypes = tuple()
_libmtp.LIBMTP_Get_First_Device.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_First_Device.restype = LIBMTP_MTPDevice_p
_libmtp.LIBMTP_Get_Folder_List_For_Storage.argtypes = LIBMTP_MTPDevice_p, c_uint32,
_libmtp.LIBMTP_Get_Folder_List_For_Storage.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Folder_List_For_Storage.restype = LIBMTP_Folder_p
_libmtp.LIBMTP_Get_Friendlyname.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Friendlyname.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Friendlyname.restype = c_char_p
_libmtp.LIBMTP_Get_Manufacturername.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Manufacturername.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Manufacturername.restype = c_char_p
_libmtp.LIBMTP_Get_Modelname.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Modelname.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Modelname.restype = c_char_p
_libmtp.LIBMTP_Get_Playlist_List.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Playlist_List.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Playlist_List.restype = LIBMTP_Playlist_p
_libmtp.LIBMTP_Get_Playlist.argtypes = LIBMTP_MTPDevice_p, c_uint32,
_libmtp.LIBMTP_Get_Playlist.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Playlist.restype = LIBMTP_Playlist_p
_libmtp.LIBMTP_Get_Serialnumber.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Get_Serialnumber.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Serialnumber.restype = c_char_p
_libmtp.LIBMTP_Get_Storage.argtypes = LIBMTP_MTPDevice_p, c_int,
_libmtp.LIBMTP_Get_Storage.errcheck = libmtp_check_return
_libmtp.LIBMTP_Get_Storage.restype = c_int
_libmtp.LIBMTP_Get_Tracklisting_With_Callback_For_Storage.argtypes = LIBMTP_MTPDevice_p, c_uint32, Progressfunc, c_void_p,
_libmtp.LIBMTP_Get_Tracklisting_With_Callback_For_Storage.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Tracklisting_With_Callback_For_Storage.restype = LIBMTP_Track_p
_libmtp.LIBMTP_Get_Trackmetadata.argtypes = LIBMTP_MTPDevice_p, c_uint32,
_libmtp.LIBMTP_Get_Trackmetadata.errcheck = libmtp_check_null
_libmtp.LIBMTP_Get_Trackmetadata.restype = LIBMTP_Track_p
_libmtp.LIBMTP_Get_Track_To_File.argtypes = LIBMTP_MTPDevice_p, c_uint32, c_char_p, Progressfunc, c_void_p,
_libmtp.LIBMTP_Get_Track_To_File.errcheck = libmtp_check_return
_libmtp.LIBMTP_Get_Track_To_File.restype = c_int
_libmtp.LIBMTP_Init.argtypes = tuple()
_libmtp.LIBMTP_Init.restype = None
_libmtp.LIBMTP_Open_Raw_Device.argtypes = LIBMTP_RawDevice_p,
_libmtp.LIBMTP_Open_Raw_Device.errcheck = libmtp_check_null
_libmtp.LIBMTP_Open_Raw_Device.restype = LIBMTP_MTPDevice_p
_libmtp.LIBMTP_Open_Raw_Device_Uncached.argtypes = LIBMTP_RawDevice_p,
_libmtp.LIBMTP_Open_Raw_Device_Uncached.errcheck = libmtp_check_null
_libmtp.LIBMTP_Open_Raw_Device_Uncached.restype = LIBMTP_MTPDevice_p
_libmtp.LIBMTP_Reset_Device.argtypes = LIBMTP_MTPDevice_p,
_libmtp.LIBMTP_Reset_Device.errcheck = libmtp_check_return
_libmtp.LIBMTP_Reset_Device.restype = c_int
_libmtp.LIBMTP_Send_File_From_File.argtypes = LIBMTP_MTPDevice_p, c_char_p, LIBMTP_File_p, Progressfunc, c_void_p,
_libmtp.LIBMTP_Send_File_From_File.errcheck = libmtp_check_return
_libmtp.LIBMTP_Send_File_From_File.restype = c_int
_libmtp.LIBMTP_Send_Track_From_File.argtypes = LIBMTP_MTPDevice_p, c_char_p, LIBMTP_Track_p, Progressfunc, c_void_p,
_libmtp.LIBMTP_Send_Track_From_File.errcheck = libmtp_check_return
_libmtp.LIBMTP_Send_Track_From_File.restype = c_int
_libmtp.LIBMTP_Set_Debug.argtypes = c_int,
_libmtp.LIBMTP_Set_Debug.restype = None
_libmtp.LIBMTP_Set_Friendlyname.argtypes = LIBMTP_MTPDevice_p, c_char_p
_libmtp.LIBMTP_Set_Friendlyname.errcheck = libmtp_check_return
_libmtp.LIBMTP_Set_Friendlyname.restype = c_int
_libmtp.LIBMTP_Update_Playlist.argtypes = LIBMTP_MTPDevice_p, LIBMTP_Playlist_p,
_libmtp.LIBMTP_Update_Playlist.errcheck = libmtp_check_return
_libmtp.LIBMTP_Update_Playlist.restype = c_int

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
	def _detect_rawdevices():
		"""
			Detects the MTP rawdevices on the USB bus that we can connect to

			@rtype: L{MTPRawDevices}
			@return: An array/list of L{MTPRawDevice} objects
		"""
		numrawdevices = c_int(0)
		rawdevices = LIBMTP_RawDevice_p()
		_libmtp.LIBMTP_Detect_Raw_Devices(byref(rawdevices), byref(numrawdevices))
		return [rawdevices[n] for n in range(numrawdevices.value)]
		libc.free(rawdevices) # TODO

	def __init__(self, cached=False, ):
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
		rawdevices = self._detect_rawdevices()
		if self.cached:
			# self.device = _libmtp.LIBMTP_Get_First_Device()
			self.device = _libmtp.LIBMTP_Open_Raw_Device(rawdevices[0])
		else:
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

	def dump_info(self):
		_libmtp.LIBMTP_Dump_Device_Info(self.device)

	def get_friendly_name(self):
		"""
			Returns the connected device's 'friendly name' (or
			known as the owner name)

			@rtype: string
			@return: The connected device's 'friendly name'
		"""
		if not self.device:
			raise NotConnected()
		return _libmtp.LIBMTP_Get_Friendlyname(self.device)

	def set_friendly_name(self, name):
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

	def get_filelisting(self, callback=0l):
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
		self._fill_cache()
		current = _libmtp.LIBMTP_Get_Filelisting_With_Callback(self.device, Progressfunc(callback), None)
		while current:
			yield dict(
				object_id=current.contents.item_id,
				parent_id=current.contents.parent_id,
				storage_id=current.contents.storage_id,
				name=current.contents.filename,
				filesize=current.contents.filesize,
				modificationdate=datetime.fromtimestamp(current.contents.modificationdate),
				filetype=LIBMTP_Filetype_reverse.get(current.contents.filetype, current.contents.filetype),
				)
			tmp = current
			current = current.contents.next
			_libmtp.LIBMTP_destroy_file_t(tmp)

	def get_files_and_folders(self, storage_id=PTP_GOH.ALL_STORAGE, parent=0):
		"""
			Returns a list of files.

			@rtype: generator
			@return: A list of the files.
		"""
		if not self.device:
			raise NotConnected()
		current = _libmtp.LIBMTP_Get_Files_And_Folders(self.device, storage_id, parent)
		while current:
			yield dict(
				object_id=current.contents.item_id,
				parent_id=current.contents.parent_id,
				storage_id=current.contents.storage_id,
				name=current.contents.filename,
				filesize=current.contents.filesize,
				modificationdate=datetime.fromtimestamp(current.contents.modificationdate),
				filetype=LIBMTP_Filetype_reverse.get(current.contents.filetype, current.contents.filetype),
				)
			tmp = current
			current = current.contents.next
			_libmtp.LIBMTP_destroy_file_t(tmp)

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

	def get_file_metadata(self, object_id):
		"""
			Returns the file metadata from the connected device

			As per the libmtp documentation, calling this function
			repeatly is not recommended, as it is slow and creates
			a large amount of USB traffic.

			@type object_id: int
			@param object_id: The unique numeric file id
			@rtype: LIBMTP_File
			@return: The file metadata
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Filemetadata(self.device, object_id)
		if not hasattr(ret, 'contents'):
			raise ObjectNotFound()
		return ret.contents

	def get_tracklist(self, callback=0l, storage_id=0):
		"""
			Returns tracks from the connected device

			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback must take two arguments, total and sent (in bytes)
			@rtype: tuple
			@return: Returns a tuple full of L{LIBMTP_Track} objects
		"""
		if not self.device:
			raise NotConnected()
		current = _libmtp.LIBMTP_Get_Tracklisting_With_Callback_For_Storage(self.device, storage_id, Progressfunc(callback), None)
		while current:
			yield dict(
				object_id=current.contents.item_id,
				parent_id=current.contents.parent_id,
				storage_id=current.contents.storage_id,
				title=current.contents.title,
				artist=current.contents.artist,
				composer=current.contents.composer,
				genre=current.contents.genre,
				album=current.contents.album,
				date=current.contents.date,
				name=current.contents.filename,
				tracknumber=current.contents.tracknumber,
				duration=current.contents.duration,
				samplerate=current.contents.samplerate,
				nochannels=current.contents.nochannels,
				wavecodec=current.contents.wavecodec,
				bitrate=current.contents.bitrate,
				bitratetype=current.contents.bitratetype,
				rating=current.contents.rating,
				usecount=current.contents.usecount,
				filesize=current.contents.filesize,
				filetype=current.contents.filetype,
				)
			tmp = current
			current = current.contents.next
			_libmtp.LIBMTP_destroy_track_t(tmp)

	def get_track_metadata(self, object_id):
		"""
			Returns the track metadata

			As per the libmtp documentation, calling this function repeatly is not
			recommended, as it is slow and creates a large amount of USB traffic.

			@type object_id: int
			@param object_id: The unique numeric track id
			@rtype: L{LIBMTP_Track}
			@return: The track metadata
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Trackmetadata(self.device, object_id)
		if not hasattr(ret, 'contents'):
			raise ObjectNotFound()
		return ret.contents

	def get_file_to_file(self, file_id, target, callback=0l):
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
		_libmtp.LIBMTP_Get_File_To_File(self.device, file_id, target, Progressfunc(callback), None)

	def get_track_to_file(self, object_id, target, callback=0l):
		"""
			Downloads the track from the connected device and stores it at
			the target location

			@type object_id: int
			@param object_id: The unique numeric track id
			@type target: str
			@param target: The location to place the track
			@type callback: function or None
			@param callback: The function provided to libmtp to receive callbacks from ptp. Callback must take two arguments, total and sent (in bytes)
		"""
		if not self.device:
			raise NotConnected()
		_libmtp.LIBMTP_Get_Track_To_File(self.device, object_id, target, Progressfunc(callback), None)

	def find_filetype(self, name):
		"""
			Attempts to guess the filetype off the name. Kind of
			inaccurate and should be trusted with a grain of salt. It
			works in most situations, though.

			@type name: str
			@param name: The name to attempt to guess from
			@rtype: int
			@return: The integer of the Filetype
		"""
		fileext = name.split(".")[-1].lower()
		for t, e in dict(
			AAC=("aac", ),
			ASF=("asf", ),
			AVI=("avi", ),
			BMP=("bmp", ),
			DOC=("doc", ),
			FLAC=("flac", ),
			GIF=("gif", ),
			JFIF=("jfif", ),
			JP2=("jp2", ),
			JPEG=("jpeg", "jpg", ),
			JPX=("jpx", ),
			M4A=("m4a", ),
			MHT=("mht", ),
			MP2=("mp2", ),
			MP3=("mp3", ),
			MP4=("mp4", ),
			MPEG=("mpeg", "mpg", ),
			OGG=("ogg", ),
			PICT=("pic", "pict", ),
			PNG=("png", ),
			PPT=("ppt", ),
			QT=("qt", "mov", ),
			TIFF=("tif", "tiff", ),
			VCALENDAR2=("ics", ),
			WAV=("wav", "wave", ),
			WINDOWSIMAGEFORMAT=("wmf", ),
			WINEXEC=("exe", "com", "bat", "dll", "sys", ),
			WMA=("wma", ),
			WMV=("wmv", ),
			XLS=("xls", ),
			XML=("xml", ),
			).items():
			if fileext in e:
				break
		else:
			t = "UNKNOWN"
		t = c_int(LIBMTP_Filetype[t])
		return t

	def send_file_from_file(self, source, target, parent=0, callback=0l):
		"""
			Sends a file from the filesystem to the connected device
			and stores it at the target name inside the parent.

			This will attempt to "guess" the filetype with
			find_filetype()

			@type source: str
			@param source: The path on the filesystem where the file resides
			@type target: str
			@param target: The target name on the device
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
		metadata = LIBMTP_File(
			filename=target,
			storage_id = 0,
			parent_id = parent,
			filetype=self.find_filetype(source),
			filesize=stat(source).st_size,
			)
		_libmtp.LIBMTP_Send_File_From_File(self.device, source, pointer(metadata), Progressfunc(callback), None)
		return dict(
			object_id=metadata.item_id,
			parent_id=metadata.parent_id,
			storage_id=metadata.storage_id,
			name=metadata.filename,
			filesize=metadata.filesize,
			modificationdate=datetime.fromtimestamp(metadata.modificationdate),
			filetype=LIBMTP_Filetype_reverse.get(metadata.filetype, metadata.filetype),
			)

	def send_track_from_file(self, source, tags, parent=0, callback=0l):
		"""
			Sends a track from the filesystem to the connected
			device

			@type source: str
			@param source: The path where the track resides
			@type target: str
			@param target: The target name on the device
			@type tags: dict
			@param tags: The track metadata
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
		metadata = LIBMTP_Track(
			filename = basename(source),
			parent_id = parent,
			storage_id = 0,
			filetype = self.find_filetype(source),
			filesize = stat(source).st_size,
			)
		for n in tags:
			setattr(metadata, n.lower(), tags[n])
		_libmtp.LIBMTP_Send_Track_From_File(self.device, source, byref(metadata), Progressfunc(callback), None)
		return dict(
			object_id=metadata.item_id,
			parent_id=metadata.parent_id,
			storage_id=metadata.storage_id,
			name=metadata.filename,
			filesize=metadata.filesize,
			modificationdate=datetime.fromtimestamp(metadata.modificationdate),
			filetype=LIBMTP_Filetype_reverse.get(metadata.filetype, metadata.filetype),
			)

	def _fill_cache(self):
		if not self.device:
			raise NotConnected()
		if not self.device.contents.storage:
			_libmtp.LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE_SORTBY.NOTSORTED)
		if not self.device.contents.storage:
			raise AssertionError('no storage')

	def get_freespace(self):
		"""
			Returns the amount of free space on the connected device
			@rtype: long
			@return: The amount of free storage in bytes
		"""
		self._fill_cache()
		return self.device.contents.storage.contents.free_space

	def get_totalspace(self):
		"""
			Returns the total space on the connected device
			@rtype: long
			@return: The amount of total storage in bytes
		"""
		self._fill_cache()
		return self.device.contents.storage.contents.max_capacity

	def get_usedspace(self):
		"""
			Returns the amount of used space on the connected device

			@rtype: long
			@return: The amount of used storage in bytes
		"""

		self._fill_cache()
		storage = self.device.contents.storage.contents
		return (storage.max_capacity - storage.free_space)

	def delete_object(self, object_id):
		"""
			Deletes the object off the connected device.

			@type object_id: int
			@param object_id: The unique object identifier
		"""

		if not self.device:
			raise NotConnected
		_libmtp.LIBMTP_Delete_Object(self.device, object_id)

	def get_playlistlist(self):
		"""
			Returns a tuple filled with L{LIBMTP_Playlist} objects
			from the connected device.

			The main gotcha of this function is that the tracks
			variable of LIBMTP_Playlist isn't iterable (without
			segfaults), so, you have to iterate over the no_tracks
			(through range or xrange) and access it that way (i.e.
			tracks[object_id]). Kind of sucks.

			@rtype: tuple
			@return: Tuple filled with LIBMTP_Playlist objects
		"""
		if not self.device:
			raise NotConnected()
		current = _libmtp.LIBMTP_Get_Playlist_List(self.device)
		while current:
			yield current.contents
			tmp = current
			current = current.contents.next
			# LIBMTP_destroy_playlist_t(tmp)

	def get_playlist(self, object_id):
		"""
			Returns a L{LIBMTP_Playlist} object of the requested
			object_id from the connected device

			@type object_id: int
			@param object_id: The unique playlist identifier
			@rtype: LIBMTP_Playlist
			@return: The playlist object
		"""
		if not self.device:
			raise NotConnected()
		ret = _libmtp.LIBMTP_Get_Playlist(self.device, object_id)
		if not ret:
			self.debug_stack(self.device)
			raise ObjectNotFound()
		return ret.contents

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
		_libmtp.LIBMTP_Create_New_Playlist(self.device, pointer(metadata), parent)

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
		_libmtp.LIBMTP_Update_Playlist(self.device, pointer(metadata))

	def get_folderlist(self, recurse=True, storage_id=0):
		"""
			Returns a pythonic generator of the folders on the
			device.

			@type recurse: bool
			@param recurse: if recurse operation is desired.
			@rtype: generator
			@return: A list of the folders on the device with id, parent-id, storage-id and name.
		"""
		if not self.device:
			raise NotConnected()
		self._fill_cache()
		folder = _libmtp.LIBMTP_Get_Folder_List_For_Storage(self.device, storage_id)
		def out(depth, folder):
			while folder:
				yield dict(
					depth=depth,
					object_id=folder.contents.folder_id,
					parent_id=folder.contents.parent_id,
					storage_id=folder.contents.storage_id,
					name=folder.contents.name,
					)
				if recurse:
					for f in out(depth+1, folder.contents.child):
						yield f
				tmp = folder
				folder = folder.contents.sibling
				if not depth:
					_libmtp.LIBMTP_destroy_folder_t(tmp)
		for f in out(0, folder):
			yield f

	def create_folder(self, name, storage, parent=0):
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
		_libmtp.LIBMTP_Create_Folder(self.device, name, parent, storage)

