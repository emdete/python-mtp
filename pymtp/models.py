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
        # Quick sanity check to make sure we don't try to
        # get an item for a NULL base_structure
        if not self.base_structure:
            raise IndexError
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
        # A quick sanity check to return 0 when base_structure
        # is null
        if not self.base_structure:
            return 0

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


class FixedArray(object):
    """
        FixedArray

        A simple list-like object that uses a list of integers and a fixed
        length. At the moment, this is used to turn those track/no_track
        attributes into a Python list.
    """

    def __init__(self, array, length, mutable=True):
        """
            Initializes the FixedArray. If None is passed as the array,
            we'll create an array of integers.

            @type array: Ctypes array
            @param array: A Ctypes array
            @type length: int
            @param length: The length of the list
        """
        self.array = array
        self.length = length
        self.mutable = mutable
        # Small sanity check
        if not self.array:
            self.array = ctypes.POINTER(ctypes.c_int(0))

    def __getitem__(self, key):
        """
            Returns the item with the index specified.

            @type key: int
            @param key: The index of the object to retrieve
        """
        if key > (self.length - 1):
            raise IndexError

        return self.array[key]

    def __delitem__(self, key):
        """
            Deletes the item at the index specified

            @type key: int
            @param key: The index of the object to delete
        """
        if not self.mutable:
            raise TypeError("Not a mutable object!")

        if key > (self.length - 1):
            raise KeyError

        for i in xrange(key, (self.length - 1)):
            self.array[i] = self.array[i + 1]

    def __setitem__(self, key, value):
        """
            Sets the value specified to the index specified

            @type key: int
            @param key: The index of the object to modify
        """
        if not self.mutable:
            raise TypeError("Not a mutable object!")

        if key > (self.length - 1):
            raise KeyError

        self.array[key] = value

    def __len__(self):
        """
            Returns the length of the array
        """
        return int(self.length)

    def append(self, value):
        """
            Appends the value specified to the end of the array
        """
        if not self.mutable:
            raise TypeError("Not a mutable object!")

        self.array[self.length - 1] = value
        self.length += 1

    def insert(self, position, value):
        """
            Inserts the value at the position specified
            @type position: int
            @param position: Index to insert the value at
        """
        if not self.mutable:
            raise TypeError("Not a mutable object!")

        if position > (self.length - 1):
            raise KeyError
        # Move the objects above the position
        for i in reversed(xrange(position, (self.length - 1))):
            self.array[i + 1] = self.array[i]

        self.array[position] = value
        self.length += 1


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


class MTPAlbum(BaseModel):
    """
        MTPAlbum

        An object representing a single album.
    """

    def _get_album_id(self):
        """
            A unique identifier for the album - typically, you don't manipulate
            this value manually.
        """
        return int(self.base_structure.album_id)

    def _set_album_id(self, value):
        self.base_structure.album_id = ctypes.c_uint32(int(value))

    album_id = property(_get_album_id, _set_album_id)

    def _get_parent_id(self):
        """
            The parent folder ID for the album
        """
        return int(self.base_structure.parent_id)

    def _set_parent_id(self, value):
        self.base_structure.parent_id = ctypes.c_uint32(int(value))

    parent_id = property(_get_parent_id, _set_parent_id)


    def _get_storage_id(self):
        """
            The unique storage identifier of the storage holding this album.

            Typically, this is the same storage as holding the tracks
            themselves.
        """
        return int(self.base_structure.storage_id)

    def _set_storage_id(self, value):
        self.base_structure.storage_id = ctypes.c_uint32(int(value))

    storage_id = property(_get_storage_id, _set_storage_id)


    def _get_name(self):
        """
            The name of the album.
        """
        return str(self.base_structure.name)

    def _set_name(self, value):
        self.base_structure.name = ctypes.c_char_p(str(value))

    name = property(_get_name, _set_name)


    def _get_artist(self):
        """
            The artist of the album
        """
        return str(self.base_structure.artist)

    def _set_artist(self, value):
        self.base_structure.artist = ctypes.c_char_p(str(value))

    artist = property(_get_artist, _set_artist)


    def _get_composer(self):
        """
            The composer of the album
        """
        return str(self.base_structure.composer)

    def _set_composer(self, value):
        self.base_structure.composer = ctypes.c_char_p(str(value))

    composer = property(_get_composer, _set_composer)


    def _get_genre(self):
        """
            The genre of the album
        """
        return str(self.base_structure.genre)

    def _set_genre(self, value):
        self.base_structure.genre = ctypes.c_char_p(str(value))

    genre = property(_get_genre, _set_genre)

    @property
    def tracks(self):
        """
            A list of tracks in the album
        """
        return FixedArray(self.base_structure.tracks,
            self.base_structure.no_tracks)


class MTPAlbums(IterableModel):
    """
        MTPAlbums

        An object representing a list of L{MTPAlbum} objects.
    """
    def __getitem__(self, key):
        """
            Returns the L{MTPAlbum} object at the index specified

            @type key: int
            @param key: Index of object to return
            @rtype: L{MTPAlbum}
            @return: The L{MTPAlbum} object at the key/index specified
        """
        return MTPAlbum(self._get_item(key))


# ---------
# Begin LIBMTP_DeviceEntry and MTPDeviceEntry
# ---------

class LIBMTP_DeviceEntry(ctypes.Structure):
    """
        LibMTP_DeviceEntry

        Contains the CTypes structure for LIBMTP_device_entry_struct
    """

    def __repr__(self):
        return "%s %s" % (self.vendor_id, self.product_id)


LIBMTP_DeviceEntry._fields_ = [
    ("vendor", ctypes.c_char_p),
    ("vendor_id", ctypes.c_uint16),
    ("product", ctypes.c_char_p),
    ("product_id", ctypes.c_uint16),
    ("device_flags", ctypes.c_uint32),
    ]


class MTPDeviceEntry(BaseModel):
    """
        MTPDeviceEntry

        An object representing a MTP device entry.
    """

    @property
    def vendor(self):
        """
            The vendor information for the device
            @rtype: str
            @return: string containing the vendor of the device
        """
        return str(self.base_structure.vendor)

    @property
    def vendor_id(self):
        """
            The Vendor ID for the device.
            @rtype: int
            @return: vendor ID
        """
        return int(self.base_structure.vendor_id)

    @property
    def product(self):
        """
            The product name for the device
            @rtype: str
            @return: string containing the product name of the device
        """
        return str(self.base_structure.product)

    @property
    def product_id(self):
        """
            The Product ID for the device
            @rtype: int
            @return: product ID
        """
        return int(self.base_structure.product_id)


# ---------
# Begin LIBMTP_DeviceStorage and MTPDeviceStorage
# ---------


class LIBMTP_DeviceStorage(ctypes.Structure):
    """
        LIBMTP_DeviceStorage

        Contains the ctypes structure for LIBMTP_devicestorage_t
    """

    def __repr__(self):
        return self.id


LIBMTP_DeviceStorage._fields_ = [
    ("storage_id", ctypes.c_uint32),
    ("storage_type", ctypes.c_uint16),
    ("filesystem_type", ctypes.c_uint16),
    ("access_capability", ctypes.c_uint16),
    ("max_capacity", ctypes.c_uint64),
    ("free_space", ctypes.c_uint64),
    ("free_space_in_objects", ctypes.c_uint64),
    ("storage_description", ctypes.c_char_p),
    ("volume_id", ctypes.c_char_p),
    ("next", ctypes.POINTER(LIBMTP_DeviceStorage)),
    ("prev", ctypes.POINTER(LIBMTP_DeviceStorage)),
    ]

class MTPDeviceStorage(BaseModel):
    """
        MTPDeviceStorage

        An object representing a MTP Device storage.
    """
    @property
    def storage_id(self):
        """
            The storage unique identifier
        """
        return int(self.base_structure.storage_id)

    @property
    def storage_type(self):
        """
            The storage type of the storage as an integer.
        """
        return int(self.base_structure.storage_type)

    @property
    def filesystem_type(self):
        """
            The filesystem type of the storage as an integer
        """
        return int(self.base_structure.filesystem_type)

    @property
    def access_capacity(self):
        """
            The accessable capacity of the storage.
        """
        return int(self.base_structure.access_capacity)

    @property
    def max_capacity(self):
        """
            The maximum capacity of the storage.
        """
        return int(self.base_structure.max_capacity)

    @property
    def free_space(self):
        """
            The amount of free space on the storage in bytes.
        """
        return int(self.base_structure.free_space)

    @property
    def free_space_in_objects(self):
        """
            The amount of free space on the storage in objects.
        """
        return int(self.base_structure.free_space_in_objects)

    @property
    def storage_description(self):
        """
            A description of the storage
        """
        return str(self.base_structure.storage_description)

    @property
    def volume_id(self):
        """
            The volume ID of the storage.
        """
        return str(self.base_structure.volume_id)

class MTPDeviceStorages(IterableModel):
    """
        MTPDeviceStorages

        An object representing a group of L{MTPDeviceStorage} objects.
    """
    def __init__(self, base_structure):
        IterableModel.__init__(self, base_structure)
        # Make sure that our base_structure refers to the "lowest" object
        # in the tree
        while True:
            if self.base_structure.prev:
                self.base_structure = self.base_structure.prev.contents
            else:
                break

    def __getitem__(self, key):
        """
            Returns the L{MTPDeviceStorage} object at the index specified.

            @type key: int
            @param key: The index of the object to retrieve
            @rtype: L{MTPDeviceStorage}
            @return: The L{MTPDeviceStorage} object at the index specified
        """
        return MTPDeviceStorage(self._get_item(key))


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


# --------
# Beginning LIBMTP_MTPDevice, MTPDevice and MTPDevices
# --------

class LIBMTP_MTPDevice(ctypes.Structure):
    """
        LIBMTP_MTPDevice

        Contains the ctypes structure for LIBMTP_mtpdevice_struct
    """

    def __repr__(self):
        return self.interface_number

LIBMTP_MTPDevice._fields_ = [
    ("object_bitsize", ctypes.c_uint8),
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
    ("next", ctypes.POINTER(LIBMTP_MTPDevice)),
    ]

class MTPDevice(BaseModel):
    """
        MTPDevice

        An object containing information about an MTP device
    """
    @property
    def storage(self):
        """
            The storage objects for the device
            @return: The device storages
            @rtype: L{MTPDeviceStorages}
        """
        return MTPDeviceStorages(self.base_structure.storage)

    @property
    def errorstack(self):
        """
            The errorstack for the device - upon initialization,
            this is set to NULL
            @return: The device's errorstack
            @rtype: L{MTPErrors}
        """
        return MTPErrors(self.base_structure.errorstack)

    @property
    def maximum_battery_level(self):
        """
            The device's maximum battery level - if LibMTP can't
            get a max battery level, this defaults to 100.
            @return: The device's maximum battery level
            @rtype: int
        """
        return int(self.base_structure.maximum_battery_level)

    @property
    def default_music_folder(self):
        """
            The ID of the default music folder
            @return: The default music folder ID
            @rtype: int
        """
        return int(self.base_structure.default_music_folder)

    @property
    def default_playlist_folder(self):
        """
            The ID of the default playlist folder
            @return: The default playlist folder ID
            @rtype: int
        """
        return int(self.base_structure.default_playlist_folder)

    @property
    def default_picture_folder(self):
        """
            The ID of the default picture folder
            @return: The default picture folder ID
            @rtype: int
        """
        return int(self.base_structure.default_picture_folder)

    @property
    def default_video_folder(self):
        """
            The ID of the default video folder
            @return: The default video folder ID
            @rtype: int
        """
        return int(self.base_structure.default_video_folder)

    @property
    def default_organizer_folder(self):
        """
            The ID of the default organizer folder
            @return: The default organizer folder ID
            @rtype: int
        """
        return int(self.base_structure.default_organizer_folder)

    @property
    def default_zencast_folder(self):
        """
            The ID of the default ZENcast folder (only on Creative devices)
            @return: The default ZENcast folder ID
            @rtype: int
        """
        return int(self.base_structure.default_zencast_folder)

    @property
    def default_album_folder(self):
        """
            The ID of the default album folder
            @return: The default album folder ID
            @rtype: int
        """
        return int(self.base_structure.default_album_folder)

    @property
    def default_text_folder(self):
        """
            The ID of the default text folder
            @return: The default text folder ID
            @rtype: int
        """
        return int(self.base_structure.default_text_folder)


class MTPDevices(IterableModel):
    """
        MTPDevices

        An object of a list of MTP devices
    """
    def __getitem__(self, key):
        """
            Returns a MTPDevice from the list of devices
            @return: The MTP device with the index specified
            @rtype: L{MTPDevice}
        """
        return MTPDevice(self._get_item(key))


# --------
# Beginning LibMTP_File, MTPFile and MTPFiles
# --------
class LIBMTP_File(ctypes.Structure):
    """
        LIBMTP_File
        Contains the ctypes structure for LIBMTP_file_t
    """

    def __repr__(self):
        return "%s (%s)" % (self.filename, self.item_id)

LIBMTP_File._fields_ = [
    ("item_id", ctypes.c_uint32),
    ("parent_id", ctypes.c_uint32),
    ("storage_id", ctypes.c_uint32),
    ("filename", ctypes.c_char_p),
    ("filesize", ctypes.c_uint64),
    ("filetype", ctypes.c_int),
    ("next", ctypes.POINTER(LIBMTP_File))
    ]

class MTPFile(BaseModel):
    """
        MTPFile

        A class representing a file on an MTP device.
    """
    @property
    def item_id(self):
        """
            The unique identifier for the file
            @return: File identifier
            @rtype: int
        """
        return int(self.base_structure.item_id)

    def _get_parent_id(self):
        """
            The ID of the parent folder
            @return: Parent folder ID
            @rtype: int
        """
        return int(self.base_structure.parent_id)

    def _set_parent_id(self, value):
        """
            Sets the parent folder ID

            Note that we don't do any sanity checks here!
        """
        self.base_structure.parent_id = ctypes.c_uint32(int(value))

    parent_id = property(_get_parent_id, _set_parent_id)

    def _get_storage_id(self):
        """
            The ID of the storage device where the file resides
            @return: Storage ID
            @rtype: int
        """
        return int(self.base_structure.storage_id)

    def _set_storage_id(self, value):
        """
            Sets the storage device ID

            As with parent_id, we don't conduct any sanity checks here
            for the values passed.
        """
        self.base_structure.storage_id = ctypes.c_uint32(int(value))

    storage_id = property(_get_storage_id, _set_storage_id)

    def _get_filename(self):
        """
            The filename of the file on the device
            @return: filename
            @rtype: str
        """
        return str(self.base_structure.filename)

    def _set_filename(self, value):
        self.base_structure.filename = ctypes.c_char_p(str(value))

    filename = property(_get_filename, _set_filename)

    def _get_filesize(self):
        """
            The size of the file in bytes
            @return: Size of file
            @rtype: int
        """
        return int(self.base_structure.filesize)

    def _set_filesize(self, value):
        self.base_structure.filesize = ctypes.c_uint64(int(value))

    filesize = property(_get_filesize, _set_filesize)

    def _get_filetype(self):
        """
            The filetype of the file
            @return: Filetype as an integer
            @rtype: int
        """
        # TODO: Maybe this should return a MTPFileType object (when they exist)
        return int(self.base_structure.filetype)

    def _set_filetype(self, value):
        # TODO: This should accept an integer AND a MTPFileType!
        self.base_structure.filetype = ctypes.c_int(int(value))

    filetype = property(_get_filetype, _set_filetype)


class MTPFiles(IterableModel):
    """
        MTPFiles

        An object representing a list of L{MTPFile} objects
    """
    def __getitem__(self, key):
        """
            Returns the L{MTPFile} object at the index specified
            @param key: The index of the object to retrieve
            @type key: int
            @return: The object requested
            @rtype: L{MTPFile}
        """
        return MTPFile(self._get_item(key))


# ----------
# Beginning LIBMTP_Track, MTPTrack and MTPTracks
# ----------
class LIBMTP_Track(ctypes.Structure):
    """
        LIBMTP_Track
        Contains the ctypes structure for LIBMTP_track_t
    """
    def __repr__(self):
        return "%s - %s (%s)" % (self.artist, self.title, self.item_id)

LIBMTP_Track._fields_ = [
    ("item_id", ctypes.c_uint32),
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
    ("next", ctypes.POINTER(LIBMTP_Track)),
    ]

class MTPTrack(BaseModel):
    """
        MTPTrack

        An object representing a music track
    """
    @property
    def item_id(self):
        """
            The track's unique identifier
            @return: Track ID
            @rtype: int
        """
        return int(self.base_structure.item_id)

    def _get_parent_id(self):
        """
            The track's parent folder ID
            @return: Parent folder ID
            @rtype: int
        """
        return int(self.base_structure.parent_id)

    def _set_parent_id(self, value):
        self.base_structure.parent_id = ctypes.c_uint32(int(value))

    parent_id = property(_get_parent_id, _set_parent_id)

    def _get_storage_id(self):
        """
            The storage ID where the track resides
            @return: Track Storage ID
            @rtype: int
        """
        return int(self.base_structure.storage_id)

    def _set_storage_id(self, value):
        self.base_structure.storage_id = ctypes.c_uint32(int(value))

    storage_id = property(_get_storage_id, _set_storage_id)

    def _get_title(self):
        """
            The title of the track
            @return: The track title
            @rtype: str
        """
        return str(self.base_structure.title)

    def _set_title(self, value):
        self.base_structure.title = ctypes.c_char_p(str(value))

    title = property(_get_title, _set_title)

    def _get_artist(self):
        """
            The recording artist of the track
            @return: The track artist
            @rtype: str
        """
        return str(self.base_structure.artist)

    def _set_artist(self, value):
        self.base_structure.artist = ctypes.c_char_p(str(value))

    artist = property(_get_artist, _set_artist)

    def _get_composer(self):
        """
            The recording composer of the track
            @return: The track composer
            @rtype: str
        """
        return str(self.base_structure.composer)

    def _set_composer(self, value):
        self.base_structure.composer = ctypes.c_char_p(str(value))

    composer = property(_get_composer, _set_composer)

    def _get_genre(self):
        """
            The genre of the track
            @return: The track genre
            @rtype: str
        """
        return str(self.base_structure.genre)

    def _set_genre(self, value):
        self.base_structure.genre = ctypes.c_char_p(str(value))

    genre = property(_get_genre, _set_genre)

    def _get_album(self):
        """
            The album name of the track
            @return: The track album
            @rtype: str
        """
        return str(self.base_structure.album)

    def _set_album(self, value):
        self.base_structure.album = ctypes.c_char_p(str(value))

    album = property(_get_album, _set_album)

    def _get_date(self):
        """
            The date of the original recording as a string
            @return: Date of the track's original recording
            @rtype: str
        """
        # TODO: change this to a datetime string?
        return str(self.base_structure.date)

    def _set_date(self, value):
        self.base_structure.date = ctypes.c_char_p(str(value))

    date = property(_get_date, _set_date)

    def _get_filename(self):
        """
            The original filename of the track
            @rtype: str
            @return: The original filename of the track
        """
        return str(self.base_structure.filename)

    def _set_filename(self, value):
        self.base_structure.filename = ctypes.c_char_p(str(value))

    filename = property(_get_filename, _set_filename)

    def _get_tracknumber(self):
        """
            The track number on the album
            @rtype: int
            @return: The track number
        """
        return int(self.base_structure.tracknumber)

    def _set_tracknumber(self, value):
        self.base_structure.tracknumber = ctypes.c_uint16(int(value))

    tracknumber = property(_get_tracknumber, _set_tracknumber)

    def _get_duration(self):
        """
            The duration of the track in milliseconds
            @rtype: int
            @return: The duration of the track in milliseconds
        """
        return int(self.base_structure.duration)

    def _set_duration(self, value):
        self.base_structure.duration = ctypes.c_uint32(int(value))

    duration = property(_get_duration, _set_duration)

    def _get_samplerate(self):
        """
            The samplerate of the track (min 0x1f80, max 0xbb80)
            @rtype: int
            @return: Samplerate of track
        """
        return int(self.base_structure.samplerate)

    def _set_samplerate(self, value):
        self.base_structure.samplerate = ctypes.c_uint32(int(value))

    samplerate = property(_get_samplerate, _set_samplerate)

    def _get_nochannels(self):
        """
            The number of channels the track has.

            If this is zero, then the number of channels is unknown.
            @rtype: int
            @return: Number of channels
        """
        return int(self.base_structure.nochannels)

    def _set_nochannels(self, value):
        self.base_structure.nochannels = ctypes.c_uint16(int(value))

    nochannels = property(_get_nochannels, _set_nochannels)

    def _get_wavecodec(self):
        """
            The FourCC wave codec ID of the track
            @rtype: int
            @return: Codec ID
        """
        return int(self.base_structure.wavecodec)

    def _set_wavecodec(self, value):
        self.base_structure.wavecodec = ctypes.c_uint32(int(value))

    wavecodec = property(_get_wavecodec, _set_wavecodec)

    def _get_bitrate(self):
        """
            The bitrate of the track (for VBR, this is the average)
            @rtype: int
            @return: Track bitrate in kbps
        """
        return int(self.base_structure.bitrate)

    def _set_bitrate(self, value):
        self.base_structure.bitrate = ctypes.c_uint32(int(value))

    bitrate = property(_get_bitrate, _set_bitrate)

# --------
# Beginning LIBMTP_Playlist, MTPPlaylist, MTPPlaylists
# --------
class LIBMTP_Playlist(ctypes.Structure):
    """
        LIBMTP_Playlist
        Contains the ctypes structure for LIBMTP_playlist_t
    """

    def __repr__(self):
        return "%s (%s)" % (self.name, self.playlist_id)

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
