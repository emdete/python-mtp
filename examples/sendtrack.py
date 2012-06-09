#!/usr/bin/env python
#
# PyMTP demo scripts
# (c) 2008 Nick Devito
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from pymtp import MTP, LIBMTP_Track
from ID3 import ID3 as id3tags

def progress(sent, total, *data):
	print('Sent {} of {} bytes'.format(sent, total))
	return 0

def main(parent, base, *files):
	if 'LIBMTP_DEBUG' in environ: MTP.set_debug(int(environ['LIBMTP_DEBUG']))
	parent = int(parent)
	with MTP(False) as mtp:
		for source in files:
			print('Sending track {}'.format(source))
			tags = id3tags(source).as_dict()
			metadata = mtp.send_track_from_file(source, tags, parent, progress)
			print("Created new track with ID: %s" % (metadata.item_id))

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

