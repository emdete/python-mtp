#!/usr/bin/env python
#
# PyMTP Demo program
# (c) 2008 Nick Devito
# Released under the GPLv3
#
from os import environ
from pymtp import MTP

def main():
	if 'LIBMTP_DEBUG' in environ: MTP.set_debug(int(environ['LIBMTP_DEBUG']))
	with MTP(True) as mtp:
		try:
			# mtp.dump_info()
			# Print out the device info
			print 'Device Name\t\t: {}'.format(mtp.get_friendly_name())
			print 'Device Manufacturer\t: {}'.format(mtp.get_manufacturer())
			print 'Device Model Name\t: {}'.format(mtp.get_modelname())
			print 'Serial Number\t\t: {}'.format(mtp.get_serialnumber())
			#print 'Battery Level\t\t: Max:{}/Cur:{}'.format(*mtp.get_batterylevel())
			print 'Total Storage\t\t: {} bytes'.format(mtp.get_totalspace())
			print 'Device Version\t\t: {}'.format(mtp.get_deviceversion())
			print 'Free Storage\t\t: {} bytes'.format(mtp.get_freespace())
			print 'Used Storage\t\t: {} bytes'.format(mtp.get_usedspace())
			# Print out the folders
			print 'Root folders\t\t:'
			for folder in mtp.get_folders(False):
				print '\t\t\t {object_id} {name}'.format(**folder)
#			# Print out the all objects
#			print 'All objects\t\t:'
#			for folder in mtp.get_files_and_folders():
#				print '\t\t\t {}'.format(folder)
			# Print out the files
			print 'File listing\t\t:'
			for devfile in mtp.get_filelisting():
				print '\t\t\t {object_id} {name} {filesize}'.format(**devfile)
			# Print out the tracks
			print 'Track listing\t\t:'
			for track in mtp.get_tracklisting():
				print '\t\t\t{object_id} {name}'.format(track)
			# Print out the playlist
			print 'Playlist listing\t\t:'
			for playlist in mtp.get_playlists():
				print '\t\t\t{object_id} {name}'.format(playlist)
				for track in playlist:
					info = mtp.get_track_metadata(track)
					print '\t\t\t\t{} - {}'.format(info.artist, info.title)
		except:
			print mtp.get_errorstack()
			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

