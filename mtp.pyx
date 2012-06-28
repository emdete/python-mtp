# -*- coding: utf-8 -*-
__author__ = 'M. Dietrich <mdt@pyneo.org>'
__version__ = '1.0.0'
__copyright__ = 'Copyright (c) 2009 M. Dietrich'
__license__ = 'GPLv3'
__docformat__ = 'reStructuredText'
'''
see file:///usr/share/doc/libmtp-doc/html/modules.html
see http://docs.cython.org/

This is a thin wrapper on libmtp. It is by far not meant to be complete.
'''
from cython import address, declare, typedef
from os import environ
from datetime import datetime
from os.path import exists, isfile
from os import stat

cdef extern from 'string.h':
	void memset(void*, int, int)

cdef extern from 'stdlib.h':
	void* malloc(int)
	void free(void*)
	ctypedef char* const_char_ptr 'const char*'

from libmtp cimport *

cdef extern from *:
	cdef enum LIBMTP_STORAGE_SORTBY: # defines from /usr/include/libmtp.h
		LIBMTP_STORAGE_SORTBY_NOTSORTED = 0
		LIBMTP_STORAGE_SORTBY_FREESPACE = 1
		LIBMTP_STORAGE_SORTBY_MAXSPACE = 2

filetypes = dict(
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
filetypes_reverse = dict([(v, n, ) for n, v in filetypes.items()])

cdef class MediaTransfer(object):
	cdef LIBMTP_mtpdevice_t* device
	cdef int cached

	def __cinit__(self, cached=False, ):
		if 'LIBMTP_DEBUG' in environ:
			self.set_debug(int(environ['LIBMTP_DEBUG']))
		self.device = NULL
		self.cached = bool(cached)

	def set_debug(self, debug):
		LIBMTP_Set_Debug(int(debug))

	def __enter__(self):
		cdef int r = 0
		cdef LIBMTP_raw_device_t* rawdevices = NULL
		cdef LIBMTP_mtpdevice_t* device_list = NULL
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

	def _cache(self):
		if not self.cached:
			r = LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE_SORTBY_NOTSORTED)
			if r not in (0, 1, ):
				raise Exception('LIBMTP_Get_Storage error={}'.format(r))
			self.cached = True

	def get_errorstack(self):
		if self.device == NULL:
			raise Exception('Not connected')
		current = LIBMTP_Get_Errorstack(self.device)
		ret = list()
		while current != NULL:
			ret.append(dict(
				errornumber=current.errornumber,
				error_text=str(current.error_text) if current.error_text != NULL else None,
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
			deviceversion=str(deviceversion) if deviceversion != NULL else None,
			friendlyname=str(friendlyname) if friendlyname != NULL else None,
			manufacturername=str(manufacturername) if manufacturername != NULL else None,
			modelname=str(modelname) if modelname != NULL else None,
			serialnumber=str(serialnumber) if serialnumber != NULL else None,
			)

	def get_storages(self):
		cdef LIBMTP_devicestorage_t* current = NULL
		cdef int r = 0
		if self.device == NULL:
			raise Exception('Not connected')
		self._cache()
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
				storage_description=str(current.StorageDescription) if current.StorageDescription != NULL else None,
				volume_identifier=str(current.VolumeIdentifier) if current.VolumeIdentifier != NULL else None,
				))
			current = current.next
		return ret

	storages = lambda self: dict([(n['storage_id'], n, ) for n in self.get_storages()])

	def get_files_and_folders(self, storage_id=0, parent_id=0, ):
		cdef LIBMTP_file_t* current = NULL
		cdef LIBMTP_file_t* tmp = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		self._cache()
		current = LIBMTP_Get_Files_And_Folders(self.device, storage_id, parent_id)
		ret = list()
		while current != NULL:
			ret.append(dict(
				filesize=str(current.filesize),
				filetype=filetypes_reverse.get(current.filetype, str(current.filetype)),
				modificationdate=datetime.fromtimestamp(current.modificationdate),
				name=str(current.filename),
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
		self._cache()
		current = LIBMTP_Get_Folder_List_For_Storage(self.device, storage_id)
		tmp = current
		ret = list()
		while current != NULL:
			ret.append(dict(
				object_id=int(current.folder_id),
				parent_id=int(current.parent_id),
				storage_id=int(current.storage_id),
				name=str(current.name) if current.name != NULL else None,
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
				filetype=filetypes_reverse.get(current.filetype, str(current.filetype)),
				))
			tmp = current
			current = current.next
			LIBMTP_destroy_file_t(tmp)
		return ret

	def get_filetype_description(self, filetype):
		cdef char* p = LIBMTP_Get_Filetype_Description(filetype)
		if p == NULL:
			return None
		return str(p)

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
			filetype=filetypes_reverse.get(current.filetype, str(current.filetype)),
			)

	def get_tracklist(self, storage_id=0, ):
		cdef LIBMTP_track_t * current = NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Tracklisting_With_Callback_For_Storage(self.device, storage_id, NULL, NULL)
		ret = list()
		while current:
			ret.append(dict(
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
				tracknumber=current.tracknumber,
				duration=current.duration,
				samplerate=current.samplerate,
				nochannels=current.nochannels,
				wavecodec=current.wavecodec,
				bitrate=current.bitrate,
				bitratetype=current.bitratetype,
				rating=current.rating,
				usecount=current.usecount,
				filesize=current.filesize,
				filetype=filetypes_reverse.get(current.filetype, str(current.filetype)),
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
			tracknumber=current.tracknumber,
			duration=current.duration,
			samplerate=current.samplerate,
			nochannels=current.nochannels,
			wavecodec=current.wavecodec,
			bitrate=current.bitrate,
			bitratetype=current.bitratetype,
			rating=current.rating,
			usecount=current.usecount,
			filesize=current.filesize,
			filetype=filetypes_reverse.get(current.filetype, str(current.filetype)),
			)

	def get_file_to_file(self, object_id, target, ):
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		r = LIBMTP_Get_File_To_File(self.device, object_id, target, NULL, NULL)
		if r != 0:
			raise Exception('LIBMTP_Get_File_To_File error={}'.format(r))

	cdef LIBMTP_filetype_t find_filetype(self, name):
		fileext = name.split('.')[-1].lower()
		for t, e in dict(
			AAC=('aac', ),
			ASF=('asf', ),
			AVI=('avi', ),
			BMP=('bmp', ),
			DOC=('doc', ),
			FLAC=('flac', ),
			GIF=('gif', ),
			JFIF=('jfif', ),
			JP2=('jp2', ),
			JPEG=('jpeg', 'jpg', ),
			JPX=('jpx', ),
			M4A=('m4a', ),
			MHT=('mht', ),
			MP2=('mp2', ),
			MP3=('mp3', ),
			MP4=('mp4', ),
			MPEG=('mpeg', 'mpg', ),
			OGG=('ogg', ),
			PICT=('pic', 'pict', ),
			PNG=('png', ),
			PPT=('ppt', ),
			QT=('qt', 'mov', ),
			TIFF=('tif', 'tiff', ),
			VCALENDAR2=('ics', ),
			WAV=('wav', 'wave', ),
			WINDOWSIMAGEFORMAT=('wmf', ),
			WINEXEC=('exe', 'com', 'bat', 'dll', 'sys', ),
			WMA=('wma', ),
			WMV=('wmv', ),
			XLS=('xls', ),
			XML=('xml', ),
			).items():
			if fileext in e:
				break
		else:
			t = 'UNKNOWN'
		return filetypes_reverse.get(t, LIBMTP_FILETYPE_UNKNOWN)

	def send_file_from_file(self, source, target, storage_id=0, parent_id=0, ):
		cdef LIBMTP_file_t current
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		if not isfile(source):
			raise IOError()
		memset(address(current), 0, sizeof(current))
		current.filename = target
		current.storage_id = storage_id
		current.parent_id = parent_id
		current.filetype = self.find_filetype(source)
		current.filesize = stat(source).st_size
		r = LIBMTP_Send_File_From_File(self.device, source, address(current), NULL, NULL)
		if r != 0:
			raise Exception('LIBMTP_Send_File_From_File error={}'.format(r))
		return dict(
			object_id=int(current.item_id),
			parent_id=current.parent_id,
			storage_id=current.storage_id,
			name=current.filename,
			filesize=current.filesize,
			modificationdate=datetime.fromtimestamp(current.modificationdate),
			filetype=filetypes_reverse.get(current.filetype, str(current.filetype)),
			)

	def send_track_from_file(self, source, target, storage_id=0, parent_id=0,
			album=None, artist=None, bitrate=None, bitratetype=None,
			composer=None, date=None, duration=None, filename=None, genre=None,
			name=None, nochannels=None, rating=None, samplerate=None,
			title=None, tracknumber=None, usecount=None, wavecodec=None, ):
		cdef LIBMTP_track_t current
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		if not exists(source):
			raise IOError()
		s = stat(source)
		memset(address(current), 0, sizeof(current))
		current.item_id = 0
		current.next = NULL
		current.filename = target
		current.filesize = s.st_size
		current.modificationdate = s.st_mtime
		#current.filetype = self.find_filetype(source) # TODO
		current.parent_id = parent_id
		current.storage_id = storage_id
		if album : current.album = album
		if artist : current.artist = artist
		if bitrate : current.bitrate = bitrate
		if bitratetype : current.bitratetype = bitratetype
		if composer : current.composer = composer
		if date : current.date = date
		if duration : current.duration = duration
		if genre : current.genre = genre
		if nochannels : current.nochannels = nochannels
		if rating : current.rating = rating
		if samplerate : current.samplerate = samplerate
		if title : current.title = title
		if tracknumber : current.tracknumber = tracknumber
		if usecount : current.usecount = usecount
		if wavecodec : current.wavecodec = wavecodec
		r = LIBMTP_Send_Track_From_File(self.device, source, address(current), NULL, NULL)
		if r != 0:
			raise Exception('LIBMTP_Send_Track_From_File error={}'.format(r))
		return dict(
			object_id=int(current.item_id),
			parent_id=current.parent_id,
			storage_id=current.storage_id,
			name=current.filename,
			filesize=current.filesize,
			modificationdate=datetime.fromtimestamp(current.modificationdate),
			filetype=filetypes_reverse.get(current.filetype, str(current.filetype)),
			)

	def get_playlistlist(self):
		cdef LIBMTP_playlist_t* current = NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Playlist_List(self.device)
		ret = list()
		while current:
			ret.append(dict(
				playlist_id=int(current.playlist_id),
				parent_id=int(current.parent_id),
				storage_id=int(current.storage_id),
				name=str(current.name) if current.name != NULL else None,
				tracks=list([current.tracks[i] for i in range(int(current.no_tracks))]),
				))
			tmp = current
			current = current.next
			LIBMTP_destroy_playlist_t(tmp)
		return ret

	def get_playlist(self, object_id):
		cdef LIBMTP_playlist_t * ret = NULL
		if not self.device:
			raise Exception('Not connected')
		ret = LIBMTP_Get_Playlist(self.device, object_id)
		return dict(
			)

	def create_new_playlist(self, name, tracks, parent_id=0, storage_id=0):
		cdef LIBMTP_playlist_t current
		cdef int no_tracks = 0
		cdef uint32_t* ts = NULL
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		memset(address(current), 0, sizeof(current))
		current.playlist_id = 0
		current.parent_id = int(parent_id)
		current.storage_id = int(storage_id)
		current.name = name
		no_tracks = int(len(tracks))
		if no_tracks > 0:
			ts = <uint32_t*>malloc(sizeof(int) * no_tracks)
			for n, object_id in enumerate(tracks):
				ts[n] = object_id
		current.tracks = ts
		current.no_tracks = no_tracks
		r = LIBMTP_Create_New_Playlist(self.device, address(current))
		free(ts)
		if r < 0:
			raise Exception('LIBMTP_Create_New_Playlist error={}'.format(r))
		return current.playlist_id

	def update_playlist(self, T, **metadata):
		cdef LIBMTP_playlist_t current
		cdef int r = 0
		if not self.device:
			raise Exception('Not connected')
		memset(address(current), 0, sizeof(current))
		r = LIBMTP_Update_Playlist(self.device, address(current))


cdef _init_module():
	LIBMTP_Init()

_init_module()
