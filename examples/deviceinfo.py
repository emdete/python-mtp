#!/usr/bin/env python
#
# PyMTP Demo program
# (c) 2008 Nick Devito
# Released under the GPLv3
#
from __future__ import print_function
from os import environ
from pymtp import MTP

def main():
	if 'LIBMTP_DEBUG' in environ: MTP.set_debug(int(environ['LIBMTP_DEBUG']))
	cache = True
	with MTP(cache) as mtp:
		try:
			mtp.dump_info()
			# Print out the device info
			print('Device Name\t\t: {}'.format(mtp.get_friendly_name()))
			print('Device Manufacturer\t: {}'.format(mtp.get_manufacturer()))
			print('Device Model Name\t: {}'.format(mtp.get_modelname()))
			print('Serial Number\t\t: {}'.format(mtp.get_serialnumber()))
			#print('Battery Level\t\t: Max:{}/Cur:{}'.format(*mtp.get_batterylevel()))
			print('Total Storage\t\t: {} bytes'.format(mtp.get_totalspace()))
			print('Device Version\t\t: {}'.format(mtp.get_deviceversion()))
			print('Free Storage\t\t: {} bytes'.format(mtp.get_freespace()))
			print('Used Storage\t\t: {} bytes'.format(mtp.get_usedspace()))
			if not cache:
				# Print out the all objects
				print('All objects\t\t\t:')
				for folder in mtp.get_files_and_folders():
					print('\t\t\t {}'.format(folder))
			# Print out the folders
			print('Root folders\t\t:')
			for obj in mtp.get_folderlist(True):
				print('\t\t\t {object_id} {name}'.format(**obj))
			# Print out the tracks
			print('Track listing\t\t:')
			for obj in mtp.get_tracklist():
				print('\t\t\t{object_id} {name}'.format(**obj))
			# Print out the playlist
			print('Playlist listing\t\t:')
			for obj in mtp.get_playlistlist():
				print('\t\t\t{object_id} {name}'.format(**obj))
				for track in obj:
					print('\t\t\t\t{} - {}'.format(**track))
			# Print out the files
			print('File listing\t\t:')
			for obj in mtp.get_filelisting():
				print('\t\t\t {object_id} {name} {filesize}'.format(**obj))
			print('Filetype-Description for 2 is: {}'.format(MTP.get_filetype_description(2)))
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

