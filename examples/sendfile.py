#!/usr/bin/env python
#
# python-mtp demo scripts
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from mtp import MediaTransfer
from os.path import basename

def main(parent, base, *files):
	parent = int(parent)
	with MediaTransfer() as mtp:
		try:
			for source in files:
				target = base + basename(source)
				print('Sending {} to {}'.format(source, target))
				metadata = mtp.send_file_from_file(source, target, parent)
				print('Created new file with metadata: {}'.format(metadata))
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

