#!/usr/bin/env python
#
# PyMTP demo scripts
# (c) 2008 Nick Devito
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from pymtp import MTP

def main(name, parent_id):
	if 'LIBMTP_DEBUG' in environ: MTP.set_debug(int(environ['LIBMTP_DEBUG']))
	with MTP() as mtp:
		try:
			parent_id = int(parent_id)
			folder_id = mtp.create_folder(name, parent_id)
			print("Created new folder with ID: {}".format(folder_id))
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == "__main__":
	from sys import argv
	main(*argv[1:])

