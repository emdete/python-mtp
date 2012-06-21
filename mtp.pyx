# -*- coding: utf-8 -*-
__author__ = "M. Dietrich <mdt@pyneo.org>"
__version__ = "prototype"
__copyright__ = "Copyright (c) 2009 M. Dietrich"
__license__ = "GPLv3"
__docformat__ = 'reStructuredText'
'''
see file:///usr/share/doc/libmtp-doc/html/modules.html
see http://docs.cython.org/

This is a thin wrapper on libmtp. it is not meant to be complete.
'''
from cython import address, declare, typedef
from os import environ
from datetime import datetime

cdef extern from "stdlib.h":
	void free(void*)
	ctypedef char* const_char_ptr "const char*"

from libmtp cimport *

cdef class MTP(object):
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
		if self.device:
			raise Exception("Already connected")
		numrawdevices = declare(int, 0)
		cdef LIBMTP_raw_device_t* rawdevices = NULL
		LIBMTP_Detect_Raw_Devices(address(rawdevices), address(numrawdevices))
		if not numrawdevices:
			raise Exception("Object not found")
		if self.cached:
			self.device = LIBMTP_Open_Raw_Device(rawdevices)
		else:
			self.device = LIBMTP_Open_Raw_Device_Uncached(rawdevices)
		free(rawdevices)
		if not self.device:
			self.device = NULL
			raise Exception("Object not found")
		LIBMTP_Clear_Errorstack(self.device)
		#LIBMTP_Reset_Device(self.device)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_value is not None:
			LIBMTP_Dump_Errorstack(self.device)
		if self.device:
			LIBMTP_Release_Device(self.device)
		self.device = NULL

	def get_errorstack(self):
		if not self.device:
			raise Exception("Not connected")
		current = LIBMTP_Get_Errorstack(self.device)
		while current:
			yield dict(
				errornumber=current.errornumber,
				error_text=current.error_text,
				)
			current = current.next

	def dump_info(self):
		LIBMTP_Dump_Device_Info(self.device)

	def set_friendly_name(self, name):
		if not self.device:
			raise Exception('Not connected')
		LIBMTP_Set_Friendlyname(self.device, name)

	def get_deviceinfo(self):
		cdef uint8_t maximum_level
		cdef uint8_t current_level
		if not self.device:
			raise Exception('Not connected')
		LIBMTP_Get_Batterylevel(self.device, address(maximum_level), address(current_level))
		return dict(
			Friendlyname=str(LIBMTP_Get_Friendlyname(self.device)),
			Serialnumber=str(LIBMTP_Get_Serialnumber(self.device)),
			Manufacturername=str(LIBMTP_Get_Manufacturername(self.device)),
			Modelname=str(LIBMTP_Get_Modelname(self.device)),
			Deviceversion=str(LIBMTP_Get_Deviceversion(self.device)),
			maximum_level=str(maximum_level),
			current_level=str(current_level),
			)

	def get_storagelist(self):
		cdef LIBMTP_devicestorage_t* current = self.device.storage
		while current:
			yield dict(
				AccessCapability=str(current.AccessCapability),
				FilesystemType=str(current.FilesystemType),
				FreeSpaceInBytes=str(current.FreeSpaceInBytes),
				FreeSpaceInObjects=str(current.FreeSpaceInObjects),
				id=str(current.id),
				MaxCapacity=str(current.MaxCapacity),
				StorageDescription=str(current.StorageDescription),
				StorageType=str(current.StorageType),
				VolumeIdentifier=str(current.VolumeIdentifier),
				)
			current = current.next

	def get_files_and_folders(self, parent_id=0, storage_id=0, ):
		cdef LIBMTP_file_t* current = NULL
		cdef LIBMTP_file_t* tmp = NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Files_And_Folders(self.device, storage_id, parent_id)
		while current:
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

	def get_files(self):
		cdef LIBMTP_file_t* tmp = NULL
		cdef LIBMTP_file_t* current = NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Filelisting_With_Callback(self.device, NULL, NULL)
		while current:
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

	def get_folders(self, recurse=True, storage_id=0, ):
		cdef LIBMTP_folder_t* current = NULL
		cdef LIBMTP_folder_t* tmp = NULL
		if not self.device:
			raise Exception('Not connected')
		current = LIBMTP_Get_Folder_List_For_Storage(self.device, storage_id)
		tmp = current
		while current:
			yield dict(
				object_id=current.folder_id,
				parent_id=current.parent_id,
				storage_id=current.storage_id,
				name=current.name,
				)
			#for f in _folder_out(recurse, depth+1, current.child): yield f # TODO
			current = current.sibling
		LIBMTP_destroy_folder_t(tmp) # LIBMTP_destroy_folder_t is recursive+enumerates!

cdef _init_module():
	LIBMTP_Init()

_init_module()
