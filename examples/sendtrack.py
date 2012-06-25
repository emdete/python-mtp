#!/usr/bin/env python
#
# python-mtp demo scripts
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from mtp import MTP
from ID3 import ID3 as id3tags

def main(parent, *files):
	parent = int(parent)
	with MTP() as mtp:
		try:
			for source in files:
				print('Sending track {}'.format(source))
				tags = id3tags(source).as_dict()
				tags['TRACKNUMBER'] = int(tags['TRACKNUMBER'])
				metadata = mtp.send_track_from_file(source, tags, parent)
				print('Created new track with metadata: {}'.format(metadata))
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

