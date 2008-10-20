#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

import os
import ctypes
import ctypes.util

from models import *
from constants import *
from errors import *

_module_path = ctypes.util.find_library("mtp")
_libmtp = ctypes.CDLL(_module_path)
# Initialize LibMTP (Why are we doing this here? Just to make sure that
# it only gets initialized once)
_libmtp.LIBMTP_Init()

# ----------
# Type Definitions
# ----------

_libmtp.LIBMTP_Get_Friendlyname.restype = ctypes.c_char_p
_libmtp.LIBMTP_Get_Serialnumber.restype = ctypes.c_char_p
_libmtp.LIBMTP_Get_Modelname.restype = ctypes.c_char_p
_libmtp.LIBMTP_Get_Manufacturername.restype = ctypes.c_char_p
_libmtp.LIBMTP_Get_Deviceversion.restype = ctypes.c_char_p
_libmtp.LIBMTP_Get_Filelisting_With_Callback.restype = ctypes.POINTER(LIBMTP_File)
_libmtp.LIBMTP_Get_Tracklisting_With_Callback.restype = ctypes.POINTER(LIBMTP_Track)
_libmtp.LIBMTP_Get_Filetype_Description.restype = ctypes.c_char_p
_libmtp.LIBMTP_Get_Filemetadata.restype = ctypes.POINTER(LIBMTP_File)
_libmtp.LIBMTP_Get_Trackmetadata.restype = ctypes.POINTER(LIBMTP_Track)
_libmtp.LIBMTP_Get_First_Device.restype = ctypes.POINTER(LIBMTP_MTPDevice)
_libmtp.LIBMTP_Get_Playlist_List.restype = ctypes.POINTER(LIBMTP_Playlist)
_libmtp.LIBMTP_Get_Playlist.restype = ctypes.POINTER(LIBMTP_Playlist)
_libmtp.LIBMTP_Get_Folder_List.restype = ctypes.POINTER(LIBMTP_Folder)
_libmtp.LIBMTP_Find_Folder.restype = ctypes.POINTER(LIBMTP_Folder)
_libmtp.LIBMTP_Get_Errorstack.restype = ctypes.POINTER(LIBMTP_Error)
# This is for callbacks with the type of LIBMTP_progressfunc_t
Progressfunc = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint64)

# ----------
# End Type Definitions
# ----------

class MTPConnectionManager(object):
    """
        MTPConnectionManager

        Provides facilities for managing connections to MTP devices
    """
    def __init__(self):
        """
            Initializes the internal structures and variables
        """
        self._mtp = _libmtp
        self.connections = {}

    def connect(self, device):
        """
            Connects to an MTP device
            @type device: L{MTPRawDevice}
            @param device: The L{MTPRawDevice} to connect to
            @rtype: L{MTPObject}
            @return: A fresh MTPObject, already connected.
        """
        if not device:
            raise ValueError
        if device.device_id in self.connections:
            raise AlreadyConnected

        obj = MTPObject(self, device)
        obj.connect()
        return obj

    def _register_object(self, obj):
        """
            Registers an object with the internal connections list
            so we don't reinitialize an MTPObject for that device
        """
        #if
        pass

class MTP:
	"""
		The MTP object
		This is the main wrapper around libmtp
	"""

	def __init__(self):
		"""
			Initializes the MTP object

			@rtype: None
			@return: None
		"""

		self.mtp = _libmtp
		self.mtp.LIBMTP_Init()
		self.device = None

	def debug_stack(self):
		"""
			Checks if __DEBUG__ is set, if so, prints and clears the
			errorstack.

			@rtype: None
			@return: None
		"""

		if __DEBUG__:
			self.mtp.LIBMTP_Dump_Errorstack()
			#self.mtp.LIBMTP_Clear_Errorstack()

	def connect(self):
		"""
			Initializes the MTP connection to the device

			@rtype: None
			@return: None

		"""

		if (self.device != None):
			raise AlreadyConnected

		self.device = self.mtp.LIBMTP_Get_First_Device()

		if not self.device:
			self.device = None
			raise NoDeviceConnected

	def disconnect(self):
		"""
			Disconnects the MTP device and deletes the self.device object

			@rtype: None
			@return: None
		"""

		if (self.device == None):
			raise NotConnected

		self.mtp.LIBMTP_Release_Device(self.device)
		del self.device
		self.device = None

	def get_devicename(self):
		"""
			Returns the connected device's 'friendly name' (or
			known as the owner name)

			@rtype: string
			@return: The connected device's 'friendly name'
		"""

		if (self.device == None):
			raise NotConnected

		return self.mtp.LIBMTP_Get_Friendlyname(self.device)

	def set_devicename(self, name):
		"""
			Changes the connected device's 'friendly name' to name

			@type name: string
			@param name: The name to change the connected device's
			 'friendly name' to
			@rtype: None
			@return: None
		"""

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Set_Friendlyname(self.device, name)
		if (ret != 0):
			self.debug_stack()
			raise CommandFailed

	def get_serialnumber(self):
		"""
			Returns the connected device's serial number

			@rtype: string
			@return: The connected device's serial number
		"""

		if (self.device == None):
			raise NotConnected

		return self.mtp.LIBMTP_Get_Serialnumber(self.device)

	def get_manufacturer(self):
		"""
			Return the connected device's manufacturer

			@rtype: string
			@return: The connected device's manufacturer
		"""
		if (self.device == None):
			raise NotConnected

		return self.mtp.LIBMTP_Get_Manufacturername(self.device)

	def get_batterylevel(self):
		"""
			Returns the connected device's maximum and current
			battery levels

			@rtype: tuple
			@return: The connected device's maximum and current
			 battery levels ([0] is maximum, [1] is current)
		"""

		if (self.device == None):
			raise NotConnected

		maximum_level = ctypes.c_uint8()
		current_level = ctypes.c_uint8()

		ret = self.mtp.LIBMTP_Get_Batterylevel(self.device, \
		  ctypes.byref(maximum_level), ctypes.byref(current_level))

		if (ret != 0):
			raise CommandFailed

		return (maximum_level.value, current_level.value)

	def get_modelname(self):
		"""
			Returns the connected device's model name (such
			as "Zen V Plus")

			@rtype: string
			@return: The connected device's model name
		"""

		if (self.device == None):
			raise NotConnected

		return self.mtp.LIBMTP_Get_Modelname(self.device)

	def get_deviceversion(self):
		"""
			Returns the connected device's version (such as
			firmware/hardware version)

			@rtype: string
			@return: Returns the connect device's version
			 information
		"""

		if (self.device == None):
			raise NotConnected

		return self.mtp.LIBMTP_Get_Deviceversion(self.device)

	def get_filelisting(self, callback=None):
		"""
			Returns the connected device's file listing as a tuple,
			containing L{LIBMTP_File} objects.

			@type callback: function or None
			@param callback: The function provided to libmtp to
			 receive callbacks from ptp. Callback must take two
			 arguments, total and sent (in bytes)
			@rtype: tuple
			@return: Returns the connect device file listing tuple
		"""

		if (self.device == None):
			raise NotConnected

		if (callback != None):
			callback = Progressfunc(callback)

		files = self.mtp.LIBMTP_Get_Filelisting_With_Callback(self.device, callback, None)
		ret = []
		next = files

		while next:
			ret.append(next.contents)
			if (next.contents.next == None):
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

		if (self.device == None):
			raise NotConnected

		return self.mtp.LIBMTP_Get_Filetype_Description(filetype)

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

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Get_Filemetadata(self.device, file_id)

		if (not hasattr(ret, 'contents')):
			raise ObjectNotFound

		return ret.contents

	def get_tracklisting(self, callback=None):
		"""
			Returns tracks from the connected device

			@type callback: function or None
			@param callback: The function provided to libmtp to
			 receive callbacks from ptp. Callback must take two
			 arguments, total and sent (in bytes)
			@rtype: tuple
			@return: Returns a tuple full of L{LIBMTP_Track} objects
		"""

		if (self.device == None):
			raise NotConnected

		if (callback != None):
			callback = Progressfunc(callback)

		tracks = self.mtp.LIBMTP_Get_Tracklisting_With_Callback(self.device, callback, None)
		ret = []
		next = tracks

		while next:
			ret.append(next.contents)
			if (next.contents.next == None):
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

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Get_Trackmetadata(self.device, track_id)

		if (not hasattr(ret, 'contents')):
			raise ObjectNotFound

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
			@param callback: The function provided to libmtp to
			 receive callbacks from ptp. Callback must take two
			 arguments, total and sent (in bytes)
		"""

		if (self.device == None):
			raise NotConnected

		if (callback != None):
			callback = Progressfunc(callback)

		ret = self.mtp.LIBMTP_Get_File_To_File(self.device, file_id, target, callback, None)

		if (ret != 0):
			self.debug_stack()
			raise CommandFailed

	def get_track_to_file(self, track_id, target, callback=None):
		"""
			Downloads the track from the connected device and stores it at
			the target location

			@type track_id: int
			@param track_id: The unique numeric track id
			@type target: str
			@param target: The location to place the track
			@type callback: function or None
			@param callback: The function provided to libmtp to
			 receive callbacks from ptp. Callback must take two
			 arguments, total and sent (in bytes)
		"""

		if (self.device == None):
			raise NotConnected

		if (callback != None):
			callback = Progressfunc(callback)

		ret = self.mtp.LIBMTP_Get_Track_To_File(self.device, track_id, target, callback, None)

		if (ret != 0):
			self.debug_stack()
			raise CommandFailed

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

		fileext = filename.lower().split(".")[-1]

		if (fileext == "wav" or fileext == "wave"):
			return LIBMTP_Filetype["WAV"]
		elif (fileext == "mp3"):
			return LIBMTP_Filetype["MP3"]
		elif (fileext == "wma"):
			return LIBMTP_Filetype["WMA"]
		elif (fileext == "ogg"):
			return LIBMTP_Filetype["OGG"]
		elif (fileext == "mp4"):
			return LIBMTP_Filetype["MP4"]
		elif (fileext == "wmv"):
			return LIBMTP_Filetype["WMV"]
		elif (fileext == "avi"):
			return LIBMTP_Filetype["AVI"]
		elif (fileext == "mpeg" or fileext == "mpg"):
			return LIBMTP_Filetype["MPEG"]
		elif (fileext == "asf"):
			return LIBMTP_Filetype["ASF"]
		elif (fileext == "qt" or fileext == "mov"):
			return LIBMTP_Filetype["QT"]
		elif (fileext == "jpeg" or fileext == "jpg"):
			return LIBMTP_Filetype["JPEG"]
		elif (fileext == "jfif"):
			return LIBMTP_Filetype["JFIF"]
		elif (fileext == "tif" or fileext == "tiff"):
			return LIBMTP_Filetype["TIFF"]
		elif (fileext == "bmp"):
			return LIBMTP_Filetype["BMP"]
		elif (fileext == "gif"):
			return LIBMTP_Filetype["GIF"]
		elif (fileext == "pic" or fileext == "pict"):
			return LIBMTP_Filetype["PICT"]
		elif (fileext == "png"):
			return LIBMTP_Filetype["PNG"]
		elif (fileext == "wmf"):
			return LIBMTP_Filetype["WINDOWSIMAGEFORMAT"]
		elif (fileext == "ics"):
			return LIBMTP_Filetype["VCALENDAR2"]
		elif (fileext == "exe" or fileext == "com" or fileext == "bat"\
		      or fileext == "dll" or fileext == "sys"):
			return LIBMTP_Filetype["WINEXEC"]
		elif (fileext == "aac"):
			return LIBMTP_Filetype["AAC"]
		elif (fileext == "mp2"):
			return LIBMTP_Filetype["MP2"]
		elif (fileext == "flac"):
			return LIBMTP_Filetype["FLAC"]
		elif (fileext == "m4a"):
			return LIBMTP_Filetype["M4A"]
		elif (fileext == "doc"):
			return LIBMTP_Filetype["DOC"]
		elif (fileext == "xml"):
			return LIBMTP_Filetype["XML"]
		elif (fileext == "xls"):
			return LIBMTP_Filetype["XLS"]
		elif (fileext == "ppt"):
			return LIBMTP_Filetype["PPT"]
		elif (fileext == "mht"):
			return LIBMTP_Filetype["MHT"]
		elif (fileext == "jp2"):
			return LIBMTP_Filetype["JP2"]
		elif (fileext == "jpx"):
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
			@param parent: The parent directory for the file to go
			 into; If 0, the file goes into main directory
			@type callback: function or None
			@param callback: The function provided to libmtp to
			 receive callbacks from ptp. Callback function must
			 take two arguments, sent and total (in bytes)
			@rtype: int
			@return: The object ID of the new file
		"""

		if (self.device == None):
			raise NotConnected

		if (os.path.isfile(source) == False):
			raise IOError

		if (callback != None):
			callback = Progressfunc(callback)

		metadata = LIBMTP_File(filename=target, \
		  filetype=self.find_filetype(source), \
		  filesize=os.stat(source).st_size)

		ret = self.mtp.LIBMTP_Send_File_From_File(self.device, source, \
		  ctypes.pointer(metadata), callback, None, parent)

		if (ret != 0):
			self.debug_stack()
			raise CommandFailed

		return metadata.item_id

	def send_track_from_file(self, source, target, metadata, parent=0, callback=None):
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
			@param parent: The parent directory for the track;
			 if 0, the track will be placed in the base dir.
			@type callback: function or None
			@param callback: The function provided to libmtp to
			 receive callbacks from ptp. Callback function must
			 take two arguments, sent and total (in bytes)
			@rtype: int
			@return: The object ID of the new track
		"""

		if (self.device == None):
			raise NotConnected

		if (os.path.exists(source) == None):
			raise IOError

		if callback:
			callback = Progressfunc(callback)

		metadata.filename = target
		metadata.parent_id = parent
		metadata.filetype = self.find_filetype(source)
		metadata.filesize = os.stat(source).st_size

		ret = self.mtp.LIBMTP_Send_Track_From_File(self.device, source, \
		  ctypes.pointer(metadata), callback, None, parent)

		if (ret != 0):
			self.debug_stack()
			raise CommandFailed

		return metadata.item_id

	def get_freespace(self):
		"""
			Returns the amount of free space on the connected device
			@rtype: long
			@return: The amount of free storage in bytes
		"""

		if (self.device == None):
			raise NotConnected

		self.mtp.LIBMTP_Get_Storage(self.device, 0)
		return self.device.contents.storage.contents.FreeSpaceInBytes

	def get_totalspace(self):
		"""
			Returns the total space on the connected device
			@rtype: long
			@return: The amount of total storage in bytes
		"""

		if (self.device == None):
			raise NotConnected

		self.mtp.LIBMTP_Get_Storage(self.device, 0)
		return self.device.contents.storage.contents.MaxCapacity

	def get_usedspace(self):
		"""
			Returns the amount of used space on the connected device

			@rtype: long
			@return: The amount of used storage in bytes
		"""

		if (self.device == None):
			raise NotConnected

		self.mtp.LIBMTP_Get_Storage(self.device, 0)
		storage = self.device.contents.storage.contents
		return (storage.MaxCapacity - storage.FreeSpaceInBytes)

	def get_usedspace_percent(self):
		"""
			Returns the amount of used space as a percentage

			@rtype: float
			@return: The percentage of used storage
		"""

		if (self.device == None):
			raise NotConnected

		self.mtp.LIBMTP_Get_Storage(self.device, 0)
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

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Delete_Object(self.device, object_id)

		if (ret != 0):
			self.debug_stack()
			raise CommandFailed

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

		if (self.device == None):
			raise NotConnected

		playlists = self.mtp.LIBMTP_Get_Playlist_List(self.device)
		ret = []
		next = playlists

		while next:
			ret.append(next.contents)
			if (next.contents.next == None):
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

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Get_Playlist(self.device, playlist_id).contents

		if (ret != 0):
			raise ObjectNotFound

		return ret

	def create_new_playlist(self, metadata, parent=0):
		"""
			Creates a new playlist based on the metadata object
			passed.

			@type metadata: LIBMTP_Playlist
			@param metadata: A LIBMTP_Playlist object describing
			 the playlist
			@type parent: int or 0
			@param parent: The parent ID or 0 for base
			@rtype: int
			@return: The object ID of the new playlist
		"""

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Create_New_Playlist(self.device, ctypes.pointer(metadata), parent)

		if (ret == 0):
			self.debug_stack()
			raise CommandFailed

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
			@param metadata: A LIBMTP_Playlist object describing
			 the updates to the playlist.
		"""

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Update_Playlist(self.device, ctypes.pointer(metadata))

		if (ret != 0):
			self.debug_stack()
			raise CommandFailed

	def get_folder_list(self):
		"""
			Returns a pythonic dict of the folders on the
			device.

			@rtype: dict
			@return: A dict of the folders on the device where
			 the folder ID is the key.
		"""

		if (self.device == None):
			raise NotConnected

		folders = self.mtp.LIBMTP_Get_Folder_List(self.device)
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

			if ((scanned == False) and (next.child)):
				## Scan the children
				next = next.child

			elif (next.sibling):
				## Scan the siblings
				next = next.sibling

			elif (next.parent_id != 0):
				## If we have no children/siblings to visit,
				## and we aren't at the parent, go back to
				## the parent.
			 	next = self.mtp.LIBMTP_Find_Folder(folders, int(next.parent_id))

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

		if (self.device == None):
			raise NotConnected
		folders = self.mtp.LIBMTP_Get_Folder_List(self.device)
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
			if (next.sibling):
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

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Create_Folder(self.device, name, parent)

		if (ret == 0):
			self.debug_stack()
			raise CommandFailed

		return ret

	def get_errorstack(self):
		"""
			Returns the connected device's errorstack from
			LIBMTP.
			@rtype: L{LIBMTP_Error}
			@return: An array of LIBMTP_Errors.
		"""

		if (self.device == None):
			raise NotConnected

		ret = self.mtp.LIBMTP_Get_Errorstack(self.device)

		if (ret != 0):
			raise CommandFailed

		return ret
