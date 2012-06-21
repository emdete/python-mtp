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

cdef extern from "stdlib.h":
	void free(void*)
	ctypedef char* const_char_ptr "const char*"

cdef extern from "libmtp.h":
	ctypedef int LIBMTP_error_number_t
	ctypedef struct LIBMTP_Album:
		pass
	ctypedef struct LIBMTP_mtpdevice_t:
		pass
	ctypedef struct LIBMTP_DeviceEntry:
		pass
	ctypedef struct LIBMTP_DeviceStorage:
		pass
	ctypedef struct LIBMTP_Error:
		pass
	ctypedef struct LIBMTP_mtpdevice_t:
		pass
	ctypedef struct LIBMTP_File:
		pass
	ctypedef struct LIBMTP_Track:
		pass
	ctypedef struct LIBMTP_Playlist:
		pass
	ctypedef struct LIBMTP_Folder:
		pass
	ctypedef struct LIBMTP_FileSampleData:
		pass
	ctypedef struct LIBMTP_error_t:
		cdef LIBMTP_error_number_t errornumber
		cdef char *error_text
		cdef LIBMTP_error_t *next
	ctypedef struct LIBMTP_raw_device_t:
		pass
	void LIBMTP_Init()
	void LIBMTP_Clear_Errorstack(LIBMTP_mtpdevice_t*)
	void LIBMTP_Create_Folder()
	void LIBMTP_Create_New_Playlist()
	void LIBMTP_Delete_Object()
	void LIBMTP_destroy_file_t()
	void LIBMTP_destroy_folder_t()
	void LIBMTP_destroy_playlist_t()
	void LIBMTP_destroy_track_t()
	LIBMTP_error_number_t LIBMTP_Detect_Raw_Devices(LIBMTP_raw_device_t**, int *)
	void LIBMTP_Dump_Device_Info()
	void LIBMTP_Dump_Errorstack(LIBMTP_mtpdevice_t*)
	void LIBMTP_Get_Batterylevel()
	void LIBMTP_Get_Deviceversion()
	LIBMTP_error_t* LIBMTP_Get_Errorstack(LIBMTP_raw_device_t*)
	void LIBMTP_Get_Filelisting_With_Callback()
	void LIBMTP_Get_Filemetadata()
	void LIBMTP_Get_Files_And_Folders()
	void LIBMTP_Get_File_To_File()
	void LIBMTP_Get_Filetype_Description()
	void LIBMTP_Get_Folder_List_For_Storage()
	void LIBMTP_Get_Friendlyname()
	void LIBMTP_Get_Manufacturername()
	void LIBMTP_Get_Modelname()
	void LIBMTP_Get_Playlist()
	void LIBMTP_Get_Playlist_List()
	void LIBMTP_Get_Serialnumber()
	void LIBMTP_Get_Storage()
	void LIBMTP_Get_Tracklisting_With_Callback_For_Storage()
	void LIBMTP_Get_Trackmetadata()
	void LIBMTP_Get_Track_To_File()
	LIBMTP_mtpdevice_t* LIBMTP_Open_Raw_Device(LIBMTP_raw_device_t*)
	LIBMTP_mtpdevice_t* LIBMTP_Open_Raw_Device_Uncached(LIBMTP_raw_device_t*)
	void LIBMTP_Release_Device(LIBMTP_mtpdevice_t*)
	void LIBMTP_Reset_Device()
	void LIBMTP_Send_File_From_File()
	void LIBMTP_Send_Track_From_File()
	void LIBMTP_Set_Debug(int)
	void LIBMTP_Set_Friendlyname()
	void LIBMTP_Update_Playlist()

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
		if exc_value:
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
				errornumber=current.contents.errornumber,
				error_text=current.contents.error_text,
				)
			current = current.contents.next


cdef _init_module():
	LIBMTP_Init()

_init_module()
