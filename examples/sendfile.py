#!/usr/bin/env python
#
# PyMTP demo scripts
# (c) 2008 Nick Devito
# Released under the GPL v3 or later.
#
from os.path import basename
from pymtp import MTP

def progress(sent, total, *data):
	return 0

def main(parent, base, *files):
	parent = int(parent)
	with MTP(False) as mtp:
		for source in files:
			target = base + basename(source)
			print 'Send {} to {}'.format(source, target)
			file_id = mtp.send_file_from_file(source, target, parent, progress)
			print "Created new track with ID: %s".format(target, file_id)

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

