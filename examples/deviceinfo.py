#!/usr/bin/env python
#
# PyMTP Demo program
# (c) 2008 Nick Devito
# Released under the GPLv3
#
from __future__ import print_function
from mtp import MTP

def main(cache):
	cache = bool(int(cache))
	with MTP(cache) as mtp:
#		try:
			#mtp.dump_info()
			# Print out the device info
			print('Device Info: {}'.format(mtp.get_deviceinfo()))
			for obj in mtp.get_storagelist():
				print('Storage id={id}'.format(**obj))
			# Print out the folders
			print('Root folders:')
			for obj in mtp.get_folders():
				print(' {object_id} {name}'.format(**obj))
			exit(0)
			# Print out the all objects
			print('Files and Folders:')
			for folder in mtp.get_files_and_folders():
				print(' {}'.format(folder))
			# Print out the tracks
			print('Track listing:')
			for obj in mtp.get_tracks():
				print(' {object_id} {name}'.format(**obj))
			# Print out the playlist
			print('Playlist listing:')
			for obj in mtp.get_playlists():
				print(' {object_id} {name}'.format(**obj))
				for track in obj:
					print(' {} - {}'.format(**track))
			# Print out the files
			print('File listing:')
			for obj in mtp.get_files():
				print(' {object_id} {name} {filesize}'.format(**obj))
			print('Filetype-Description for 2 is: {}'.format(MTP.get_filetype_description(2)))
#		except:
#			for n in mtp.get_errorstack():
#				print('{errornumber}: {error_text}'.format(**n))
#			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

