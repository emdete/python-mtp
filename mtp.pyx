# -*- coding: utf-8 -*-
# see file:///usr/share/doc/libmtp-doc/html/modules.html
# see http://docs.cython.org/
# cython: language_level=3
''' This is a thin wrapper on libmtp to be used with python.
'''

__author__ = 'M. Dietrich <mdt@pyneo.org>'
__version__ = '1.0.0'
__copyright__ = 'Copyright (c) 2009 M. Dietrich'
__license__ = 'GPLv3'
__docformat__ = 'reStructuredText'

from cython import address, declare, typedef
from os import environ
from datetime import datetime
from os.path import exists, isfile
from os import stat

cdef extern from 'stdlib.h':
	void* malloc(int)
	void free(void*)
	ctypedef char* const_char_ptr 'const char*'
	char* strdup(const_char_ptr)
	void memset(void*, int, int)

from libmtp cimport *

cdef extern from *:
	cdef enum LIBMTP_STORAGE_SORTBY: # #defines from /usr/include/libmtp.h
		LIBMTP_STORAGE_SORTBY_NOTSORTED = 0
		LIBMTP_STORAGE_SORTBY_FREESPACE = 1
		LIBMTP_STORAGE_SORTBY_MAXSPACE = 2
	cdef enum LIBMTP_DEBUG: # #defines from /usr/include/libmtp.h
		LIBMTP_DEBUG_NONE = 0x00
		LIBMTP_DEBUG_PTP = 0x01
		LIBMTP_DEBUG_PLST = 0x02
		LIBMTP_DEBUG_USB = 0x04
		LIBMTP_DEBUG_DATA = 0x08
		LIBMTP_DEBUG_ALL = 0xFF

_filetypes = dict(
	AAC=LIBMTP_FILETYPE_AAC, ALBUM=LIBMTP_FILETYPE_ALBUM,
	ASF=LIBMTP_FILETYPE_ASF, AUDIBLE=LIBMTP_FILETYPE_AUDIBLE,
	AVI=LIBMTP_FILETYPE_AVI, BMP=LIBMTP_FILETYPE_BMP, DOC=LIBMTP_FILETYPE_DOC,
	FIRMWARE=LIBMTP_FILETYPE_FIRMWARE, FLAC=LIBMTP_FILETYPE_FLAC,
	FOLDER=LIBMTP_FILETYPE_FOLDER, GIF=LIBMTP_FILETYPE_GIF,
	HTML=LIBMTP_FILETYPE_HTML, JFIF=LIBMTP_FILETYPE_JFIF,
	JP2=LIBMTP_FILETYPE_JP2, JPEG=LIBMTP_FILETYPE_JPEG,
	JPX=LIBMTP_FILETYPE_JPX, M4A=LIBMTP_FILETYPE_M4A,
	MEDIACARD=LIBMTP_FILETYPE_MEDIACARD, MHT=LIBMTP_FILETYPE_MHT,
	MP2=LIBMTP_FILETYPE_MP2, MP3=LIBMTP_FILETYPE_MP3, MP4=LIBMTP_FILETYPE_MP4,
	MPEG=LIBMTP_FILETYPE_MPEG, OGG=LIBMTP_FILETYPE_OGG,
	PICT=LIBMTP_FILETYPE_PICT, PLAYLIST=LIBMTP_FILETYPE_PLAYLIST,
	PNG=LIBMTP_FILETYPE_PNG, PPT=LIBMTP_FILETYPE_PPT, QT=LIBMTP_FILETYPE_QT,
	TEXT=LIBMTP_FILETYPE_TEXT, TIFF=LIBMTP_FILETYPE_TIFF,
	UNDEF_AUDIO=LIBMTP_FILETYPE_UNDEF_AUDIO,
	UNDEF_VIDEO=LIBMTP_FILETYPE_UNDEF_VIDEO, UNKNOWN=LIBMTP_FILETYPE_UNKNOWN,
	VCALENDAR1=LIBMTP_FILETYPE_VCALENDAR1,
	VCALENDAR2=LIBMTP_FILETYPE_VCALENDAR2, VCARD2=LIBMTP_FILETYPE_VCARD2,
	VCARD3=LIBMTP_FILETYPE_VCARD3, WAV=LIBMTP_FILETYPE_WAV,
	WINDOWSIMAGEFORMAT=LIBMTP_FILETYPE_WINDOWSIMAGEFORMAT,
	WINEXEC=LIBMTP_FILETYPE_WINEXEC, WMA=LIBMTP_FILETYPE_WMA,
	WMV=LIBMTP_FILETYPE_WMV, XLS=LIBMTP_FILETYPE_XLS, XML=LIBMTP_FILETYPE_XML,
	)

_filetypes_reverse = dict([(v, n, ) for n, v in _filetypes.items()])

_filetypes_extensions = dict(
	AAC=('aac', ), ASF=('asf', ), AVI=('avi', ), BMP=('bmp', ), DOC=('doc', ),
	FLAC=('flac', ), GIF=('gif', ), JFIF=('jfif', ), JP2=('jp2', ),
	JPEG=('jpeg', 'jpg', ), JPX=('jpx', ), M4A=('m4a', ), MHT=('mht', ),
	MP2=('mp2', ), MP3=('mp3', ), MP4=('mp4', ), MPEG=('mpeg', 'mpg', ),
	OGG=('ogg', ), PICT=('pic', 'pict', ), PNG=('png', ), PPT=('ppt', ),
	QT=('qt', 'mov', ), TIFF=('tif', 'tiff', ), VCALENDAR2=('ics', ),
	WAV=('wav', 'wave', ), WINDOWSIMAGEFORMAT=('wmf', ), WINEXEC=('exe', 'com',
	'bat', 'dll', 'sys', ), WMA=('wma', ), WMV=('wmv', ), XLS=('xls', ),
	XML=('xml', ),
	)


cdef class MediaTransfer(object):
	'''This is the low-level wrapper class for libmtp. It more or less exposes
	all the LIBMTP_ functions directly with no boilerplate.

	set the environment var LIBMTP_DEBUG to enable debugging (for valid values
	see file:///usr/share/doc/libmtp-doc/html/group__internals.html#LIBMTP_Set_Debug).
	'''
	cdef LIBMTP_mtpdevice_t* device
	cdef int cached

	def __cinit__(self, cached=False, ):
		'''init the object and set LIBMTP_Set_Debug from env
		'''
		if 'LIBMTP_DEBUG' in environ:
			self._set_debug(int(environ['LIBMTP_DEBUG']))
		self.device = NULL
		self.cached = bool(cached)

	cdef void _set_debug(self, int debug):
		LIBMTP_Set_Debug(int(debug))

	def __enter__(self):
		'''
		'''
		cdef int r = 0
		cdef LIBMTP_raw_device_t* rawdevices = NULL
		#cdef LIBMTP_mtpdevice_t* device_list = NULL
		cdef int numrawdevices = 0
		if self.device:
			raise Exception('Already connected')
		r = LIBMTP_Detect_Raw_Devices(address(rawdevices), address(numrawdevices))
		if r != 0:
			raise Exception('LIBMTP_Detect_Raw_Devices error={}'.format(r))
		if not numrawdevices:
			raise Exception('Zero devices found')
		if self.cached:
			self.device = LIBMTP_Open_Raw_Device(rawdevices)
			# cached alternatives:
			#self.device = LIBMTP_Get_First_Device()
			#if LIBMTP_Get_Connected_Devices(&device_list) == 0: self.device = device_list
		else:
			self.device = LIBMTP_Open_Raw_Device_Uncached(rawdevices)
		free(rawdevices)
		if self.device == NULL:
			raise Exception('LIBMTP_Open_Raw_Device[_Uncached] failed')
		LIBMTP_Reset_Device(self.device)
		LIBMTP_Clear_Errorstack(self.device)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_value is not None:
			LIBMTP_Dump_Errorstack(self.device)
			LIBMTP_Clear_Errorstack(self.device)
		if self.device != NULL:
			LIBMTP_Release_Device(self.device)
		self.device = NULL
		return False

	cdef LIBMTP_file_t* _cache(self, int storage_id, int parent_id):
		if not self.cached:
			r = LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE_SORTBY_NOTSORTED)
			if r not in (0, 1, ):
				raise Exception('LIBMTP_Get_Storage error={}'.format(r))
			self.cached = True
		return LIBMTP_Get_Files_And_Folders(self.device, storage_id, parent_id)

	def get_errorstack(self):
		if self.device == NULL:
			raise Exception('Not connected')
		current = LIBMTP_Get_Errorstack(self.device)
		ret = list()
		while current != NULL:
			ret.append(dict(
				errornumber=current.errornumber,
				error_text=current.error_text if current.error_text != NULL else None,
				))
			current = current.next
		LIBMTP_Clear_Errorstack(self.device)
		return ret

	def dump_info(self):
		LIBMTP_Dump_Device_Info(self.device)

	def set_friendly_name(self, name):
		if self.device == NULL:
			raise Exception('Not connected')
		LIBMTP_Set_Friendlyname(self.device, name)

	def get_deviceinfo(self):
		cdef uint8_t maximum_level = 0
		cdef uint8_t current_level = 0
		cdef char* deviceversion = NULL
		cdef char* friendlyname = NULL
		cdef char* manufacturername = NULL
		cdef char* modelname = NULL
		cdef char* serialnumber = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		LIBMTP_Get_Batterylevel(self.device, address(maximum_level), address(current_level))
		deviceversion = LIBMTP_Get_Deviceversion(self.device)
		friendlyname = LIBMTP_Get_Friendlyname(self.device)
		manufacturername = LIBMTP_Get_Manufacturername(self.device)
		modelname = LIBMTP_Get_Modelname(self.device)
		serialnumber = LIBMTP_Get_Serialnumber(self.device)
		return dict(
			battery_current_level=int(current_level),
			battery_maximum_level=int(maximum_level),
			deviceversion=deviceversion if deviceversion != NULL else None,
			friendlyname=friendlyname if friendlyname != NULL else None,
			manufacturername=manufacturername if manufacturername != NULL else None,
			modelname=modelname if modelname != NULL else None,
			serialnumber=serialnumber if serialnumber != NULL else None,
			maximum_battery_level=self.device.maximum_battery_level,
			default_music_folder=self.device.default_music_folder if self.device.default_music_folder != 0xffffffff else None,
			default_playlist_folder=self.device.default_playlist_folder if self.device.default_playlist_folder != 0xffffffff else None,
			default_picture_folder=self.device.default_picture_folder if self.device.default_picture_folder != 0xffffffff else None,
			default_video_folder=self.device.default_video_folder if self.device.default_video_folder != 0xffffffff else None,
			default_organizer_folder=self.device.default_organizer_folder if self.device.default_organizer_folder != 0xffffffff else None,
			default_zencast_folder=self.device.default_zencast_folder if self.device.default_zencast_folder != 0xffffffff else None,
			default_album_folder=self.device.default_album_folder if self.device.default_album_folder != 0xffffffff else None,
			default_text_folder=self.device.default_text_folder if self.device.default_text_folder != 0xffffffff else None,
			)

	def get_storages(self):
		cdef LIBMTP_devicestorage_t* current = NULL
		cdef int r = 0
		if self.device == NULL:
			raise Exception('Not connected')
		self._cache(0, 0)
		current = self.device.storage
		ret = list()
		while current != NULL:
			ret.append(dict(
				access_capability=int(current.AccessCapability),
				filesystem_type=int(current.FilesystemType),
				free_space_in_bytes=int(current.FreeSpaceInBytes),
				free_space_in_objects=int(current.FreeSpaceInObjects),
				max_capacity=int(current.MaxCapacity),
				storage_id=int(current.id),
				storage_type=int(current.StorageType),
				storage_description=current.StorageDescription if current.StorageDescription != NULL else None,
				volume_identifier=current.VolumeIdentifier if current.VolumeIdentifier != NULL else None,
				))
			current = current.next
		return ret

	storages = property(lambda self: dict([(n['storage_id'], n, ) for n in self.get_storages()]))

	def get_files_and_folders(self, storage_id=0, parent_id=0, ):
		cdef LIBMTP_file_t* current = NULL
		cdef LIBMTP_file_t* tmp = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		current = self._cache(storage_id, parent_id)
		ret = list()
		while current != NULL:
			ret.append(dict(
				filesize=int(current.filesize),
				filetype=_filetypes_reverse.get(current.filetype, str(current.filetype)),
				modificationdate=datetime.fromtimestamp(current.modificationdate),
				name=current.filename,
				object_id=int(current.item_id),
				parent_id=int(current.parent_id),
				storage_id=int(current.storage_id),
				))
			tmp = current
			current = current.next
			LIBMTP_destroy_file_t(tmp)
		return ret

	objects = lambda self, storage_id: dict([(n['object_id'], n, ) for n in self.get_files_and_folders(storage_id)])

	def create_folder(self, name, storage_id, parent_id=0):
		cdef uint32_t r = 0
		if not self.device:
			raise Exception('Not connected')
		r = LIBMTP_Create_Folder(self.device, name, parent_id, storage_id)
		if r <= 0:
			raise Exception('LIBMTP_Create_Folder error={}'.format(r))
		return r

	def get_folders(self, storage_id=0, recurse=False, ):
		cdef LIBMTP_folder_t* current = NULL
		cdef LIBMTP_folder_t* tmp = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		self._cache(storage_id, 0)
		current = LIBMTP_Get_Folder_List_For_Storage(self.device, storage_id)
		tmp = current
		ret = list()
		while current != NULL:
			ret.append(dict(
				object_id=int(current.folder_id),
				parent_id=int(current.parent_id),
				storage_id=int(current.storage_id),
				name=current.name if current.name != NULL else None,
				))
			#for f in _folder_out(recurse, depth+1, current.child): yield f # TODO
			current = current.sibling
		LIBMTP_destroy_folder_t(tmp) # LIBMTP_destroy_folder_t is recursive+enumerates!
		return ret

	def get_files(self):
		cdef LIBMTP_file_t* tmp = NULL
		cdef LIBMTP_file_t* current = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		self._cache(0, 0)
		current = LIBMTP_Get_Filelisting_With_Callback(self.device, NULL, NULL)
		ret = list()
		while current != NULL:
			ret.append(dict(
				object_id=int(current.item_id),
				parent_id=current.parent_id,
				storage_id=current.storage_id,
				name=current.filename,
				filesize=current.filesize,
				modificationdate=datetime.fromtimestamp(current.modificationdate),
				filetype=_filetypes_reverse.get(current.filetype, str(current.filetype)),
				))
			tmp = current
			current = current.next
			LIBMTP_destroy_file_t(tmp)
		return ret

	# cdef const_char_ptr p = LIBMTP_Get_Filetype_Description(filetype)

	def delete_object(self, object_id):
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		r = LIBMTP_Delete_Object(self.device, object_id)
		if r != 0:
			raise Exception('LIBMTP_Delete_Object error={}'.format(r))
		return r

	def get_metadata(self, object_id):
		cdef LIBMTP_file_t* NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Filemetadata(self.device, object_id)
		return dict(
			object_id=int(current.item_id),
			parent_id=current.parent_id,
			storage_id=current.storage_id,
			name=current.filename,
			filesize=current.filesize,
			modificationdate=datetime.fromtimestamp(current.modificationdate),
			filetype=_filetypes_reverse.get(current.filetype, str(current.filetype)),
			)

	def get_tracks(self, storage_id=0, ):
		cdef LIBMTP_track_t * current = NULL
		if not self.device:
			raise Exception('Not connected')
		self._cache(0, 0)
		current = LIBMTP_Get_Tracklisting_With_Callback_For_Storage(self.device, storage_id, NULL, NULL)
		ret = list()
		while current:
			ret.append(dict(
				object_id=int(current.item_id),
				parent_id=int(current.parent_id),
				storage_id=int(current.storage_id),
				title=current.title if current.title != NULL else None,
				artist=current.artist if current.artist != NULL else None,
				composer=current.composer if current.composer != NULL else None,
				genre=current.genre if current.genre != NULL else None,
				album=current.album if current.album != NULL else None,
				date=current.date if current.date != NULL else None,
				name=current.filename if current.filename != NULL else None,
				tracknumber=int(current.tracknumber),
				duration=int(current.duration),
				samplerate=int(current.samplerate),
				nochannels=int(current.nochannels),
				wavecodec=int(current.wavecodec),
				bitrate=int(current.bitrate),
				bitratetype=int(current.bitratetype),
				rating=int(current.rating),
				usecount=int(current.usecount),
				filesize=int(current.filesize),
				filetype=_filetypes_reverse.get(current.filetype, str(current.filetype)),
				))
			tmp = current
			current = current.next
			LIBMTP_destroy_track_t(tmp)
		return ret

	def get_track_metadata(self, object_id):
		cdef LIBMTP_track_t * current = NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Trackmetadata(self.device, object_id)
		return dict(
			object_id=int(current.item_id),
			parent_id=current.parent_id,
			storage_id=current.storage_id,
			title=current.title,
			artist=current.artist,
			composer=current.composer,
			genre=current.genre,
			album=current.album,
			date=current.date,
			name=current.filename,
			tracknumber=int(current.tracknumber),
			duration=current.duration,
			samplerate=current.samplerate,
			nochannels=current.nochannels,
			wavecodec=current.wavecodec,
			bitrate=current.bitrate,
			bitratetype=current.bitratetype,
			rating=current.rating,
			usecount=current.usecount,
			filesize=current.filesize,
			filetype=_filetypes_reverse.get(current.filetype, str(current.filetype)),
			)

	def get_file_to_file(self, object_id, target, ):
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		r = LIBMTP_Get_File_To_File(self.device, object_id, target, NULL, NULL)
		if r != 0:
			raise Exception('LIBMTP_Get_File_To_File error={}'.format(r))

	cdef LIBMTP_filetype_t find_filetype(self, name):
		extension = name.split('.')[-1].lower()
		for filetype, extensions in _filetypes_extensions.items():
			if extension in extensions:
				return _filetypes.get(filetype, LIBMTP_FILETYPE_UNKNOWN)
		return LIBMTP_FILETYPE_UNKNOWN

	def send_file_from_file(self, source, target, storage_id=0, parent_id=0, ):
		cdef LIBMTP_file_t* current = NULL
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		if not isfile(source):
			raise IOError()
		current = LIBMTP_new_file_t()
		if current == NULL:
			raise Exception('LIBMTP_new_file_t failed')
		try:
			current.filename = target
			current.storage_id = storage_id
			current.parent_id = parent_id
			current.filetype = self.find_filetype(source)
			current.filesize = stat(source).st_size
			r = LIBMTP_Send_File_From_File(self.device, source, current, NULL, NULL)
			if r != 0:
				raise Exception('LIBMTP_Send_File_From_File error={}'.format(r))
			return dict(
				object_id=int(current.item_id),
				parent_id=current.parent_id,
				storage_id=current.storage_id,
				name=current.filename,
				filesize=current.filesize,
				modificationdate=datetime.fromtimestamp(current.modificationdate),
				filetype=_filetypes_reverse.get(current.filetype, str(current.filetype)),
				)
		finally:
			current.filename = NULL
			LIBMTP_destroy_file_t(current)

	def send_track_from_file(self, source, target, storage_id=0, parent_id=0,
			album=None, artist=None, bitrate=None, bitratetype=None,
			composer=None, date=None, duration=None, filename=None, genre=None,
			name=None, nochannels=None, rating=None, samplerate=None,
			title=None, tracknumber=None, usecount=None, wavecodec=None, **unused):
		cdef LIBMTP_track_t* current = NULL
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		if not exists(source):
			raise IOError()
		current = LIBMTP_new_track_t()
		if current == NULL:
			raise Exception('LIBMTP_new_file_t failed')
		try:
			s = stat(source)
			current.item_id = 0
			current.next = NULL
			current.filename = target
			current.filesize = s.st_size
			current.modificationdate = s.st_mtime
			current.filetype = self.find_filetype(source)
			current.parent_id = parent_id
			current.storage_id = storage_id
			if album : current.album = album
			if artist : current.artist = artist
			if bitrate : current.bitrate = int(bitrate)
			if bitratetype : current.bitratetype = int(bitratetype)
			if composer : current.composer = composer
			if date : current.date = date
			if duration : current.duration = int(duration)
			if genre : current.genre = genre
			if nochannels : current.nochannels = int(nochannels)
			if rating : current.rating = int(rating)
			if samplerate : current.samplerate = int(samplerate)
			if title : current.title = title
			if tracknumber : current.tracknumber = int(tracknumber)
			if usecount : current.usecount = int(usecount)
			if wavecodec : current.wavecodec = int(wavecodec)
			r = LIBMTP_Send_Track_From_File(self.device, source, current, NULL, NULL)
			if r != 0:
				raise Exception('LIBMTP_Send_Track_From_File error={}'.format(r))
			return dict(
				object_id=int(current.item_id),
				parent_id=current.parent_id,
				storage_id=current.storage_id,
				name=current.filename,
				filesize=current.filesize,
				modificationdate=datetime.fromtimestamp(current.modificationdate),
				filetype=_filetypes_reverse.get(current.filetype, str(current.filetype)),
				)
		finally:
			current.album = NULL
			current.artist = NULL
			current.composer = NULL
			current.date = NULL
			current.filename = NULL
			current.genre = NULL
			current.title = NULL
			LIBMTP_destroy_track_t(current)

	def get_playlists(self):
		cdef LIBMTP_playlist_t* current = NULL
		if not self.device:
			raise Exception('Not connected')
		self._cache(0, 0)
		current = LIBMTP_Get_Playlist_List(self.device)
		tmp = current
		ret = list()
		while current:
			ret.append(dict(
				object_id=int(current.playlist_id),
				parent_id=int(current.parent_id),
				storage_id=int(current.storage_id),
				name=current.name if current.name != NULL else None,
				tracks=list([current.tracks[i] for i in range(int(current.no_tracks))]),
				))
			current = current.next
		LIBMTP_destroy_playlist_t(tmp)
		return ret

	def get_playlist(self, object_id):
		cdef LIBMTP_playlist_t * current = NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Playlist(self.device, object_id)
		if current == NULL:
			raise Exception('LIBMTP_Get_Playlist failed')
		return dict(
			object_id=int(current.playlist_id),
			parent_id=int(current.parent_id),
			storage_id=int(current.storage_id),
			name=current.name if current.name != NULL else None,
			tracks=list([current.tracks[i] for i in range(int(current.no_tracks))]),
			)

	def create_playlist(self, name, tracks, parent_id=0, storage_id=0):
		cdef LIBMTP_playlist_t* current = NULL
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_new_playlist_t()
		if current == NULL:
			raise Exception('LIBMTP_new_playlist_t failed')
		try:
			current.playlist_id = 0
			current.parent_id = int(parent_id)
			current.storage_id = int(storage_id)
			current.name = name
			current.next = NULL
			current.tracks = NULL
			current.no_tracks = int(len(tracks))
			if current.no_tracks > 0:
				current.tracks = <uint32_t*>malloc(sizeof(int) * current.no_tracks)
				memset(current.tracks, 0, sizeof(int) * current.no_tracks)
				for n, object_id in enumerate(tracks):
					current.tracks[n] = object_id
			r = LIBMTP_Create_New_Playlist(self.device, current)
			if r < 0:
				raise Exception('LIBMTP_Create_New_Playlist error={}'.format(r))
			return current.playlist_id
		finally:
			if current.tracks != NULL:
				free(current.tracks)
				current.tracks = NULL # libmtp will free() this otherwise
			current.name = NULL # libmtp will free() this otherwise
			LIBMTP_destroy_playlist_t(current)

	def update_playlist(self, **metadata):
		cdef LIBMTP_playlist_t* current = NULL
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_new_playlist_t()
		if current == NULL:
			raise Exception('LIBMTP_new_playlist_t failed')
		try:
			r = LIBMTP_Update_Playlist(self.device, current)
			if r < 0:
				raise Exception('LIBMTP_Update_Playlist error={}'.format(r))
			return current.playlist_id
		finally:
			current.name = NULL # libmtp will free() this otherwise
			LIBMTP_destroy_playlist_t(current)


cdef _init_module():
	LIBMTP_Init()

_init_module()
