#!/usr/bin/env python
#
# PyMTP demo scripts
# (c) 2008 Nick Devito
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from pymtp import MTP, LIBMTP_Playlist

def main(name, *tracks):
	with MTP() as mtp:
		try:
			metadata = LIBMTP_Playlist()
			for track in tracks:
				metadata.append(track)
			playlist_id = mtp.create_new_playlist(name, metadata)
			print("Created new playlist with ID: {}".format(playlist_id))
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == "__main__":
	from sys import argv
	main(*argv[1:])
