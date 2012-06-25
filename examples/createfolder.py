#!/usr/bin/env python
#
# python-mtp demo scripts
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from mtp import MediaTransfer

def main(name, parent_id):
	with MediaTransfer() as mtp:
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

