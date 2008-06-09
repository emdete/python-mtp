#!/usr/bin/env python
#
# PyMTP Demo program
# (c) 2008 Nick Devito
# Released under the GPL-3
#

import sys
sys.path.insert(0, "../") # so the examples work out of the box

import pymtp

# Connect to MTP
mtp = pymtp.MTP()
mtp.connect()

# Print out the device info
print "Device Name\t\t: %s" % (mtp.get_devicename())
print "Device Manufacturer\t: %s" % (mtp.get_manufacturer())
print "Device Model Name\t: %s" % (mtp.get_modelname())
print "Serial Number\t\t: %s" % (mtp.get_serialnumber())
print "Battery Level\t\t: Max:%s/Cur:%s (%s%%)" % (mtp.get_batterylevel()[0], mtp.get_batterylevel()[1], ((float(mtp.get_batterylevel()[1])/float(mtp.get_batterylevel()[0]))*100))
print "Device Version\t\t: %s" % (mtp.get_deviceversion())
print "Total Storage\t\t: %s bytes" % (mtp.get_totalspace())
print "Free Storage\t\t: %s bytes" % (mtp.get_freespace())
print "Used Storage\t\t: %s bytes (%s%%)" % (mtp.get_usedspace(), ((float(mtp.get_usedspace()) / float(mtp.get_totalspace())*100)))
## Print out the folders
print "Parent folders\t\t:"
for folder in mtp.get_parent_folders():
	print "\t\t\t %s (id: %s)" % (folder.name, folder.folder_id)

print "All folders\t\t:"
folders = mtp.get_folder_list()
for key in folders:
	folder = folders[key]
	print "\t\t\t %s (id: %s, parent: %s)" % (folder.name, folder.folder_id, folder.parent_id)

## Print out the file and track listings
print "File listing\t\t:"
for devfile in mtp.get_filelisting():
	print "\t\t\t %s (id: %s / %s bytes)" % (devfile.filename, devfile.item_id, devfile.filesize)

print "Track listing\t\t:"
for track in mtp.get_tracklisting():
	print "\t\t\t%s - %s (%s / %s bytes)" % (track.artist, track.title, track.filename, track.filesize)
print "Playlist listing\t\t:"
for playlist in mtp.get_playlists():
	print "\t\t\t%s (id: %s / %s tracks)" % (playlist.name, playlist.playlist_id, playlist.no_tracks)
	for track in playlist:
		info = mtp.get_track_metadata(track)
		print "\t\t\t\t%s - %s" % (info.artist, info.title)

## Disconnect from the device
mtp.disconnect()
