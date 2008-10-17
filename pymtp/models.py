#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# PyMTP
# Developed by: Nick Devito (nick@nick125.com)
# (c) 2008 Nick Devito
# Released under the GPLv3 or later.
#

"""
	Provides the nice comfy data models for PyMTP.
"""

import sets
import ctypes

# ----------
# BaseModel Definition
# ----------

class BaseModel(object):
	"""
		BaseModel
		
		Provides a basic model for Pythonic PyMTP data structures
	"""
	def __init__(self, base_structure):
		"""
			Initializes a BaseModel for the supplied base_structure.
			
			@param base_structure: The underlying CTypes structure to "wrap".
			@type base_structure: any ctypes.structure object
			@return: Nothing
		"""
		self.base_structure = base_structure
		
class IterableModel(BaseModel):
	"""
		IterableModel
		
		Provides a basic iterable model for CTypes data types that specify
		a "next" parameter (as a pointer).
		
		You still have to define __getitem__, etc, but you can use _get_item 
		to retrieve the object!
	"""
	
	def _get_item(self, level):
		"""
		Returns the "level"th object in the list. If the level exceeds
		the number of objects in the list, it'll raise IndexError.
		
		@type level: int
		@param key: The index of the object to retrieve
		@return: The CTypes data type object
		@rtype: CTypes data type
		"""
		current = self.base_structure
		for i in xrange(level):
			if current.next:
				current = current.next.contents
				else:
					raise IndexError
				
				return current
				
	def __len__(self):
		"""
			Returns the number of objects in the list.
			B{Note that this function is really expensive!}
			
			@return: the number of objects in the list
			@rtype: int
		"""
		level = 0
		current = self.base_structure
		while True:
			if current.next:
				level += 1
				current = current.next.contents
			else:
				return level
				
				
class MutableIterableModel(IterableModel):
	"""
		MutableIterableModel
		
		Extends the L{IterableModel} model for mutable objects.
		
		As with L{IterableModel}, you still have to provide the data type
		functions (i.e., __getitem__, __setitem__, __delitem__, etc), but you
		can use the functions in this model to perform the underlying 
		operations.
	"""
	pass


# ---------
# Defining LIBMTP_Album, MTPAlbum and MTPAlbums
# ---------

class LIBMTP_Album(ctypes.Structure):
	"""
		LIBMTP_Album
	
		Contains the ctypes structure for LIBMTP_album_struct
	"""
	
	def __repr__(self):
		return str(self.name)

LIBMTP_Album._fields_ = [
	("album_id", ctypes.c_uint32),
	("parent_id", ctypes.c_uint32),
	("storage_id", ctypes.c_uint32),
	("name", ctypes.c_char_p),
	("artist", ctypes.c_char_p),
	("composer", ctypes.c_char_p),
	("genre", ctypes.c_char_p),
	("tracks", ctypes.POINTER(ctypes.c_uint32)),
	("no_tracks", ctypes.c_uint32),
	("next", ctypes.POINTER(LIBMTP_Album)),
	]

# ---------
# Defining LIBMTP_Error, MTPError, and MTPErrors
# ---------

class LIBMTP_Error(ctypes.Structure):
	"""
		LIBMTP_Error
		
		Contains the ctypes structure for LIBMTP_error_struct
	"""

	def __repr__(self):
		return int(self.errornumber)

LIBMTP_Error._fields_ = [
	("errornumber", ctypes.c_int),
	("error_text", ctypes.c_char_p),
	("next", ctypes.POINTER(LIBMTP_Error)),
	]
						 
class MTPError(BaseModel):
	"""
		MTPError
		
		An object representing an single MTP error.
	"""
	@property
	def errornumber(self):
		"""
			Returns the error number
			
			@return: LibMTP error number
			@rtype: int
		"""
		return int(self.base_structure.errornumber)

	@property
	def error_text(self):
		"""
			Returns the error text
			
			@return: LibMTP error text
			@rtype: str
		"""
		return str(self.base_structure.error_text)
		
		
class MTPErrors(IterableModel):
	"""
		MTPErrors
		
		An object representing a list of MTPError objects.
	"""	
		
	def __getitem__(self, key):
		"""
			Returns the key from the list of errors
			
			@type key: int
			@param key: The index of the object to retrieve
			@return: A MTPError object
			@rtype: L{MTPError}
		"""
		return MTPError(self._get_item(key))



class LIBMTP_DeviceStorage(ctypes.Structure):
	"""
		LIBMTP_DeviceStorage
		Contains the ctypes structure for LIBMTP_devicestorage_t
	"""

	def __repr__(self):
		return self.id

LIBMTP_DeviceStorage._fields_ = [("id", ctypes.c_uint32),
                                 ("StorageType", ctypes.c_uint16),
                                 ("FilesystemType", ctypes.c_uint16),
                                 ("AccessCapability", ctypes.c_uint16),
                                 ("MaxCapacity", ctypes.c_uint64),
                                 ("FreeSpaceInBytes", ctypes.c_uint64),
                                 ("FreeSpaceInObjects", ctypes.c_uint64),
                                 ("StorageDescription", ctypes.c_char_p),
                                 ("VolumeIdentifier", ctypes.c_char_p),
                                 ("next", ctypes.POINTER(LIBMTP_DeviceStorage)),
                                 ("prev", ctypes.POINTER(LIBMTP_DeviceStorage))]

class LIBMTP_MTPDevice(ctypes.Structure):
	"""
		LIBMTP_MTPDevice
		Contains the ctypes structure for LIBMTP_mtpdevice_t
	"""

	def __repr__(self):
		return self.interface_number

LIBMTP_MTPDevice._fields_ = [("interface_number", ctypes.c_uint8),
                             ("params", ctypes.c_void_p),
                             ("usbinfo", ctypes.c_void_p),
                             ("storage", ctypes.POINTER(LIBMTP_DeviceStorage)),
                             ("errorstack", ctypes.POINTER(LIBMTP_Error)),
                             ("maximum_battery_level", ctypes.c_uint8),
                             ("default_music_folder", ctypes.c_uint32),
                             ("default_playlist_folder", ctypes.c_uint32),
                             ("default_picture_folder", ctypes.c_uint32),
                             ("default_video_folder", ctypes.c_uint32),
                             ("default_organizer_folder", ctypes.c_uint32),
                             ("default_zencast_folder", ctypes.c_uint32),
                             ("default_album_folder", ctypes.c_uint32),
                             ("default_text_folder", ctypes.c_uint32),
                             ("cd", ctypes.c_void_p),
                             ("next", ctypes.POINTER(LIBMTP_MTPDevice))]

class LIBMTP_File(ctypes.Structure):
	"""
		LIBMTP_File
		Contains the ctypes structure for LIBMTP_file_t
	"""

	def __repr__(self):
		return "%s (%s)" % (self.filename, self.item_id)

LIBMTP_File._fields_ = [("item_id", ctypes.c_uint32),
                        ("parent_id", ctypes.c_uint32),
                        ("storage_id", ctypes.c_uint32),
                        ("filename", ctypes.c_char_p),
                        ("filesize", ctypes.c_uint64),
			("filetype", ctypes.c_int),
			("next", ctypes.POINTER(LIBMTP_File))]

class LIBMTP_Track(ctypes.Structure):
	"""
		LIBMTP_Track
		Contains the ctypes structure for LIBMTP_track_t
	"""

	def __repr__(self):
		return "%s - %s (%s)" % (self.artist, self.title, self.item_id)
		
LIBMTP_Track._fields_ = [("item_id", ctypes.c_uint32),
			("parent_id", ctypes.c_uint32),
                        ("storage_id", ctypes.c_uint32),
			("title", ctypes.c_char_p),
			("artist", ctypes.c_char_p),
			("composer", ctypes.c_char_p), 
			("genre", ctypes.c_char_p),
			("album", ctypes.c_char_p),
			("date", ctypes.c_char_p),
			("filename", ctypes.c_char_p),
			("tracknumber", ctypes.c_uint16),
			("duration", ctypes.c_uint32),
			("samplerate", ctypes.c_uint32),
			("nochannels", ctypes.c_uint16),
			("wavecodec", ctypes.c_uint32),
			("bitrate", ctypes.c_uint32),
			("bitratetype", ctypes.c_uint16),
			("rating", ctypes.c_uint16),
			("usecount", ctypes.c_uint32),
			("filesize", ctypes.c_uint64),
			("filetype", ctypes.c_int),
			("next", ctypes.POINTER(LIBMTP_Track))]

class LIBMTP_Playlist(ctypes.Structure):
	"""
		LIBMTP_Playlist
		Contains the ctypes structure for LIBMTP_playlist_t
	"""

	def __init__(self):
		self.tracks = ctypes.pointer(ctypes.c_uint32(0))
		self.no_tracks = ctypes.c_uint32(0)
	def __repr__(self):
		return "%s (%s)" % (self.name, self.playlist_id)

	def __iter__(self):
		"""
			This allows the playlist object to act like a list with
			a generator.
		"""
		for track in xrange(self.no_tracks):
			yield self.tracks[track]

	def __getitem__(self, key):
		"""
			This allows the playlist to return tracks like a list
		"""

		if (key > (self.no_tracks - 1)):
			raise IndexError

		return self.tracks[key]

	def __setitem__(self, key, value):
		"""
			This allows the user to manipulate the playlist like a 
			list. However, this will only modify existing objects, 
			you can't try to set a key outside of the current size.
		"""

		if (key > (self.no_tracks - 1)):
			raise IndexError

		self.tracks[key] = value

	def __delitem__(self, key):
		"""
			This allows the user to delete an object
			from the playlist
		"""

		if (key > (self.no_tracks - 1)):
			raise IndexError

		for i in range(key, (self.no_tracks - 1)):
			self.tracks[i] = self.tracks[i + 1]

		self.no_tracks -= 1
	
	def append(self, value):
		"""
			This function appends a track to the end of the tracks
			list.
		"""
		if (self.tracks == None):
			self.tracks = ctypes.pointer(ctypes.c_uint32(0))

		self.no_tracks += 1
		self.tracks[(self.no_tracks - 1)] = value

	def __len__(self):
		"""
			This returns the number of tracks in the playlist
		"""

		return self.no_tracks

LIBMTP_Playlist._fields_ = [("playlist_id", ctypes.c_uint32),
                            ("parent_id", ctypes.c_uint32),
                            ("storage_id", ctypes.c_uint32),
                            ("name", ctypes.c_char_p),
                            ("tracks", ctypes.POINTER(ctypes.c_uint32)),
                            ("no_tracks", ctypes.c_uint32),
                            ("next", ctypes.POINTER(LIBMTP_Playlist))]

class LIBMTP_Folder(ctypes.Structure):
	"""
		LIBMTP_Folder
		Contains the ctypes structure for LIBMTP_folder_t
	"""

	def __repr__(self):
		return "%s (%s)" % (self.name, self.folder_id)

LIBMTP_Folder._fields_ = [("folder_id", ctypes.c_uint32),
                          ("parent_id", ctypes.c_uint32),
                          ("storage_id", ctypes.c_uint32),
                          ("name", ctypes.c_char_p),
                          ("sibling", ctypes.POINTER(LIBMTP_Folder)),
                          ("child", ctypes.POINTER(LIBMTP_Folder))]
