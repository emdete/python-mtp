#!/usr/bin/env python
#
# python-mtp demo scripts
# Released under the GPL v3 or later.
#
from __future__ import print_function
from os import environ
from mtp import MediaTransfer

def main(*object_ids):
	with MediaTransfer() as mtp:
		try:
			for object_id in object_ids:
				mtp.delete_object(int(object_id))
				print("Deleted object {}".format(object_id))
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

