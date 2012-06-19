# -*- coding: utf-8 -*-
__author__ = "M. Dietrich <mdt@pyneo.org>"
__version__ = "prototype"
__copyright__ = "Copyright (c) 2009 M. Dietrich"
__license__ = "GPLv3"
__docformat__ = 'reStructuredText'
'''
see file:///usr/share/doc/libmtp-doc/html/modules.html

This is a thin wrapper on libmtp. it is not meant to be complete.
'''

cdef extern from *:
	ctypedef char* const_char_ptr "const char*"

cdef extern from "libmtp.h":
	ctypedef struct LIBMTP_Album:
		pass
	ctypedef struct LIBMTP_DeviceEntry:
		pass
	ctypedef struct LIBMTP_DeviceStorage:
		pass
	ctypedef struct LIBMTP_Error:
		pass
	ctypedef struct LIBMTP_MTPDevice:
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
	ctypedef struct LIBMTP_RawDevice:
		pass
	void LIBMTP_Init()
	void LIBMTP_Clear_Errorstack()
	void LIBMTP_Create_Folder()
	void LIBMTP_Create_New_Playlist()
	void LIBMTP_Delete_Object()
	void LIBMTP_destroy_file_t()
	void LIBMTP_destroy_folder_t()
	void LIBMTP_destroy_playlist_t()
	void LIBMTP_destroy_track_t()
	void LIBMTP_Detect_Raw_Devices()
	void LIBMTP_Dump_Device_Info()
	void LIBMTP_Dump_Errorstack()
	void LIBMTP_Get_Batterylevel()
	void LIBMTP_Get_Deviceversion()
	void LIBMTP_Get_Errorstack()
	void LIBMTP_Get_Filelisting_With_Callback()
	void LIBMTP_Get_Filemetadata()
	void LIBMTP_Get_Files_And_Folders()
	void LIBMTP_Get_File_To_File()
	void LIBMTP_Get_Filetype_Description()
	void LIBMTP_Get_First_Device()
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
	void LIBMTP_Init()
	void LIBMTP_Open_Raw_Device()
	void LIBMTP_Open_Raw_Device_Uncached()
	void LIBMTP_Reset_Device()
	void LIBMTP_Send_File_From_File()
	void LIBMTP_Send_Track_From_File()
	void LIBMTP_Set_Debug()
	void LIBMTP_Set_Friendlyname()
	void LIBMTP_Update_Playlist()

cdef _init_module():
	LIBMTP_Init()

_init_module()
