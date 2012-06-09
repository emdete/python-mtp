#!/usr/bin/env python
#
# PyMTP Demo program
# (c) 2008 Nick Devito
# Released under the GPLv3
#
from pymtp import MTP

def main():
	MTP.set_debug(255)
	with MTP() as mtp:
		# mtp.dump_info()
		# Print out the device info
		print "Device Name\t\t: {}".format(mtp.get_devicename())
		print "Device Manufacturer\t: {}".format(mtp.get_manufacturer())
		print "Device Model Name\t: {}".format(mtp.get_modelname())
		print "Serial Number\t\t: {}".format(mtp.get_serialnumber())
		print "Battery Level\t\t: Max:{}/Cur:{}".format(*mtp.get_batterylevel())
		print "Total Storage\t\t: {} bytes".format(mtp.get_totalspace())
		print "Device Version\t\t: {}".format(mtp.get_deviceversion())
		print "Free Storage\t\t: {} bytes".format(mtp.get_freespace())
		print "Used Storage\t\t: {} bytes ({}%%)".format(mtp.get_usedspace(), ((float(mtp.get_usedspace()) / float(mtp.get_totalspace())*100)))
		# Print out the folders
		print "Parent folders\t\t:"
		for folder in mtp.get_parent_folders():
			print "\t\t\t {} (id: {})".format(folder.name, folder.folder_id)
		print "All folders\t\t:"
		folders = mtp.get_folder_list()
		for key in folders:
			folder = folders[key]
			print "\t\t\t {} (id: {}, parent: {})".format(folder.name, folder.folder_id, folder.parent_id)
		# Print out the file and track listings
		print "File listing\t\t:"
		for devfile in mtp.get_filelisting():
			print "\t\t\t {} (id: {} / {} bytes)".format(devfile.filename, devfile.item_id, devfile.filesize)
		print "Track listing\t\t:"
		for track in mtp.get_tracklisting():
			print "\t\t\t{} - {} ({} / {} bytes)".format(track.artist, track.title, track.filename, track.filesize)
		print "Playlist listing\t\t:"
		for playlist in mtp.get_playlists():
			print "\t\t\t{} (id: {} / {} tracks)".format(playlist.name, playlist.playlist_id, playlist.no_tracks)
			for track in playlist:
				info = mtp.get_track_metadata(track)
				print "\t\t\t\t{} - {}".format(info.artist, info.title)

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

