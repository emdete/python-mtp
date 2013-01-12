#!/usr/bin/env python
#
# python-mtp demo scripts
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from os.path import basename
from mtp import MediaTransfer
from ID3 import ID3 as id3tags

def upload_track(mtp, parent_id, source):
	metadata = dict([(n.lower(), v, ) for n, v in id3tags(source).as_dict().items()])
	metadata = mtp.send_track_from_file(source, 'Music/' + basename(source), parent_id=parent_id, **metadata)
	print("Created new track with ID: {object_id}".format(**metadata))
	return metadata['object_id']

def main(name, *files):
	with MediaTransfer() as mtp:
		try:
#			for playlist in mtp.get_playlists():
#				print('playlist={}'.format(playlist))
			parent_id = mtp.get_deviceinfo()['default_music_folder'] or 0xffffffff
			tracks = list()
			for track in files:
				track = upload_track(mtp, parent_id, track)
				tracks.append(track)
			parent_id = mtp.get_deviceinfo()['default_playlist_folder'] or 0
			object_id = mtp.create_playlist(name, tracks, parent_id)
			print("Created new playlist with ID: {object_id}".format(object_id=object_id))
			print('{}'.format(mtp.get_playlist(object_id)))
			mtp.update_playlist(object_id, None, tracks)
		except Exception, e:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise e

if __name__ == "__main__":
	from sys import argv
	main(*argv[1:])
