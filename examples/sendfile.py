#!/usr/bin/env python
#
# PyMTP demo scripts
# (c) 2008 Nick Devito
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os.path import basename
from os import environ
from pymtp import MTP

def progress(sent, total, *data):
	print('Sent {} of {} bytes'.format(sent, total))
	return 0

def main(parent, base, *files):
	if 'LIBMTP_DEBUG' in environ: MTP.set_debug(int(environ['LIBMTP_DEBUG']))
	parent = int(parent)
	with MTP() as mtp:
		for source in files:
			target = base + basename(source)
			print('Sending {} to {}'.format(source, target))
			metadata = mtp.send_file_from_file(source, target, parent, progress)
			print('Created new file with metadata: {}'.format(metadata))

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

