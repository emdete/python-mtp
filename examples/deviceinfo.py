#!/usr/bin/env python
#
# python-mtp Demo program
# Released under the GPLv3
#
from __future__ import print_function
from mtp import MTP

def main(cached):
	cached = bool(int(cached))
	with MTP(cached) as mtp:
		try:
			mtp.dump_info()
			print('Infos:')
			for n, m in mtp.get_deviceinfo().items():
				print('Info {}={}'.format(n, m))
			print('Storages:')
			for obj in mtp.get_storages():
				print('Storage "{storage_description}" id={object_id} {free_space_in_bytes}/{max_capacity}bytes'.format(**obj))
			print('Files:')
			for obj in mtp.get_files():
				print(' {object_id} {name} {filesize}'.format(**obj))
			if not cached:
				print('Files and Folders:')
				for obj in mtp.get_files_and_folders():
					print(' {}'.format(obj))
			print('Folders:')
			for obj in mtp.get_folders():
				print(' {object_id} {name}'.format(**obj))
			print('Tracklists:')
			for obj in mtp.get_tracks():
				print(' {object_id} {name}'.format(**obj))
			print('Playlists:')
			for obj in mtp.get_playlists():
				print(' {object_id} {name}'.format(**obj))
				for track in obj:
					print(' {} - {}'.format(**track))
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

