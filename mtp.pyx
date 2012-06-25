# -*- coding: utf-8 -*-
__author__ = "M. Dietrich <mdt@pyneo.org>"
__version__ = "prototype"
__copyright__ = "Copyright (c) 2009 M. Dietrich"
__license__ = "GPLv3"
__docformat__ = 'reStructuredText'
'''
see file:///usr/share/doc/libmtp-doc/html/modules.html
see http://docs.cython.org/

This is a thin wrapper on libmtp. It is by far not meant to be complete.
'''
from cython import address, declare, typedef
from os import environ
from datetime import datetime
from os.path import exists, isfile, basename
from os import stat

cdef extern from "stdlib.h":
	void free(void*)
	ctypedef char* const_char_ptr "const char*"

from libmtp cimport *

cdef extern from *:
	cdef enum LIBMTP_STORAGE_SORTBY: # defines from /usr/include/libmtp.h
		LIBMTP_STORAGE_SORTBY_NOTSORTED = 0
		LIBMTP_STORAGE_SORTBY_FREESPACE = 1
		LIBMTP_STORAGE_SORTBY_MAXSPACE = 2

cdef class _MTP(object):
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
		cdef LIBMTP_raw_device_t* rawdevices = NULL
		cdef LIBMTP_mtpdevice_t* device_list = NULL
		cdef int numrawdevices = 0
		if self.device:
			raise Exception("Already connected")
		if LIBMTP_Detect_Raw_Devices(address(rawdevices), address(numrawdevices)) != 0:
			raise Exception('Detect failed')
		if not numrawdevices:
			raise Exception("Object not found")
		if self.cached:
			self.device = LIBMTP_Open_Raw_Device(rawdevices)
			# cached alternatives:
			#self.device = LIBMTP_Get_First_Device()
			#if LIBMTP_Get_Connected_Devices(&device_list) == 0: self.device = device_list
		else:
			self.device = LIBMTP_Open_Raw_Device_Uncached(rawdevices)
#		free(rawdevices)
		if self.device == NULL:
			raise Exception("Device not found")
#		LIBMTP_Reset_Device(self.device)
#		LIBMTP_Clear_Errorstack(self.device)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
#		if exc_value is not None:
#			LIBMTP_Dump_Errorstack(self.device)
#			LIBMTP_Clear_Errorstack(self.device)
#		if self.device != NULL:
#			LIBMTP_Release_Device(self.device)
#		self.device = NULL
		return True

	def _cache(self):
		if not self.cached:
			r = LIBMTP_Get_Storage(self.device, LIBMTP_STORAGE_SORTBY_NOTSORTED)
			if r not in (0, 1, ):
				raise Exception('Get storage failed with error={}'.format(r))
			self.cached = True

	def get_errorstack(self):
		if self.device == NULL:
			raise Exception("Not connected")
		current = LIBMTP_Get_Errorstack(self.device)
		while current != NULL:
			yield dict(
				errornumber=current.errornumber,
				error_text=str(current.error_text) if current.error_text != NULL else None,
				)
			current = current.next
		LIBMTP_Clear_Errorstack(self.device)

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
		while current != NULL:
			yield dict(
				access_capability=int(current.AccessCapability),
				filesystem_type=int(current.FilesystemType),
				free_space_in_bytes=int(current.FreeSpaceInBytes),
				free_space_in_objects=int(current.FreeSpaceInObjects),
				max_capacity=int(current.MaxCapacity),
				object_id=int(current.id),
				storage_type=int(current.StorageType),
				storage_description=str(current.StorageDescription) if current.StorageDescription != NULL else None,
				volume_identifier=str(current.VolumeIdentifier) if current.VolumeIdentifier != NULL else None,
				)
			current = current.next

	def get_files_and_folders(self, parent_id=0, storage_id=0, ):
		cdef LIBMTP_file_t* current = NULL
		cdef LIBMTP_file_t* tmp = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		self._cache()
		current = LIBMTP_Get_Files_And_Folders(self.device, storage_id, parent_id)
		print('got them {}'.format(<int>current))
		while current != NULL:
			yield dict(
				filesize=str(current.filesize),
				filetype=str(current.filetype), # TODO reverse map to string
				modificationdate=datetime.fromtimestamp(current.modificationdate),
				name=str(current.filename),
				object_id=str(current.item_id),
				parent_id=str(current.parent_id),
				storage_id=str(current.storage_id),
				)
			tmp = current
			current = current.next
			LIBMTP_destroy_file_t(tmp)

	def get_folders(self, storage_id=0, recurse=False, ):
		cdef LIBMTP_folder_t* current = NULL
		cdef LIBMTP_folder_t* tmp = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		self._cache()
		current = LIBMTP_Get_Folder_List_For_Storage(self.device, storage_id)
		tmp = current
		while current != NULL:
			yield dict(
				object_id=int(current.folder_id),
				#parent_id=int(current.parent_id),
				#storage_id=int(current.storage_id),
				#name=str(current.name) if current.name != NULL else None,
				)
			#for f in _folder_out(recurse, depth+1, current.child): yield f # TODO
			current = current.sibling
		LIBMTP_destroy_folder_t(tmp) # LIBMTP_destroy_folder_t is recursive+enumerates!

	def get_files(self):
		cdef LIBMTP_file_t* tmp = NULL
		cdef LIBMTP_file_t* current = NULL
		if self.device == NULL:
			raise Exception('Not connected')
		current = LIBMTP_Get_Filelisting_With_Callback(self.device, NULL, NULL)
		while current != NULL:
			yield dict(
				object_id=current.item_id,
				parent_id=current.parent_id,
				storage_id=current.storage_id,
				name=current.filename,
				filesize=current.filesize,
				modificationdate=datetime.fromtimestamp(current.modificationdate),
				filetype=current.filetype, # TODO map to string
				)
			tmp = current
			current = current.next
			LIBMTP_destroy_file_t(tmp)

	def get_filetype_description(self, filetype):
		return LIBMTP_Get_Filetype_Description(filetype)
	def get_file_metadata(self, object_id):
		if not self.device:
			raise Exception('Not connected')
		ret = LIBMTP_Get_Filemetadata(self.device, object_id)
		return dict(
			)
	def get_tracklist(self, storage_id=0, ):
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Tracklisting_With_Callback_For_Storage(self.device, storage_id, NULL, NULL)
		while current:
			yield dict(
				object_id=current.item_id,
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
				filetype=current.filetype,
				)
			tmp = current
			current = current.next
			LIBMTP_destroy_track_t(tmp)
	def get_track_metadata(self, object_id):
		if not self.device:
			raise Exception('Not connected')
		ret = LIBMTP_Get_Trackmetadata(self.device, object_id)
		return dict(
			)
	def get_file_to_file(self, file_id, target, ):
		if not self.device:
			raise Exception('Not connected')
		LIBMTP_Get_File_To_File(self.device, file_id, target, NULL, NULL)
	def get_track_to_file(self, object_id, target, ):
		if not self.device:
			raise Exception('Not connected')
		LIBMTP_Get_Track_To_File(self.device, object_id, target, NULL, NULL)
	def find_filetype(self, name):
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
		return t
	def send_file_from_file(self, source, target, storage_id=0, parent_id=0, ):
		if not self.device:
			raise Exception('Not connected')
		if not isfile(source):
			raise IOError()
		cdef LIBMTP_file_t metadata
		# TODO metadata.filename=target,
		metadata.storage_id = storage_id,
		metadata.parent_id = parent_id,
		# TODO metadata.filetype=self.find_filetype(source),
		metadata.filesize=stat(source).st_size,
		LIBMTP_Send_File_From_File(self.device, source, address(metadata), NULL, NULL)
		return dict(
			object_id=metadata.item_id,
			parent_id=metadata.parent_id,
			storage_id=metadata.storage_id,
			name=metadata.filename,
			filesize=metadata.filesize,
			modificationdate=datetime.fromtimestamp(metadata.modificationdate),
			# TODO filetype=metadata.filetype, # TODO
			)
	def send_track_from_file(self, source, tags, storage_id=0, parent_id=0, ):
		if not self.device:
			raise Exception('Not connected')
		if not exists(source):
			raise IOError()
		cdef LIBMTP_track_t metadata
		# TODO metadata.filename = basename(source),
		metadata.parent_id = parent_id,
		metadata.storage_id = storage_id,
		# TODO metadata.filetype = self.find_filetype(source),
		metadata.filesize = stat(source).st_size,
		# TODO for n in tags: setattr(metadata, n.lower(), tags[n])
		LIBMTP_Send_Track_From_File(self.device, source, address(metadata), NULL, NULL)
		return dict(
			object_id=metadata.item_id,
			parent_id=metadata.parent_id,
			storage_id=metadata.storage_id,
			name=metadata.filename,
			filesize=metadata.filesize,
			modificationdate=datetime.fromtimestamp(metadata.modificationdate),
			# TODO filetype=metadata.filetype, # TODO
			)
	def delete_object(self, object_id):
		if not self.device:
			raise Exception('Not connected')
		LIBMTP_Delete_Object(self.device, object_id)
	def get_playlistlist(self):
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Playlist_List(self.device)
		while current:
			yield dict(
				)
			tmp = current
			current = current.next
			LIBMTP_destroy_playlist_t(tmp)
	def get_playlist(self, object_id):
		if not self.device:
			raise Exception('Not connected')
		ret = LIBMTP_Get_Playlist(self.device, object_id)
		return dict(
			)
	def create_new_playlist(self, TODO, parent_id=0):
		if not self.device:
			raise Exception('Not connected')
		cdef LIBMTP_playlist_t metadata
		LIBMTP_Create_New_Playlist(self.device, address(metadata))
	def update_playlist(self, TODO):
		if not self.device:
			raise Exception('Not connected')
		cdef LIBMTP_playlist_t metadata
		LIBMTP_Update_Playlist(self.device, address(metadata))
	def create_folder(self, name, storage, parent_id=0):
		if not self.device:
			raise Exception('Not connected')
		LIBMTP_Create_Folder(self.device, name, parent_id, storage)


class MTP(_MTP):
	def __init__(self, cached):
		pass

cdef _init_module():
	LIBMTP_Init()

_init_module()
