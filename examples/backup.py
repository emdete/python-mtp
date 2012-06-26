#!/usr/bin/env python
#
# python-mtp Demo program
# Released under the GPLv3
#
from __future__ import print_function
from mtp import MediaTransfer
from os.path import dirname
from os import makedirs

def determine_name(objects, name, parent_id=None, **v):
	if not parent_id:
		return name
	return determine_name(objects, **objects[parent_id]) + '/' + name

def main():
	with MediaTransfer() as mtp:
		try:
			info = mtp.get_deviceinfo()
			#print('Backup serialnumber: "{serialnumber}"'.format(**info))
			base = info['serialnumber']
			for storage_id, storage in mtp.storages().items():
				#print('Backup storage: "{storage_description}"'.format(**storage))
				base = base + '/' + storage['storage_description']
				objects = mtp.objects(storage_id)
				for object_id, _object in objects.items():
					if _object['filetype'] != 'FOLDER':
						name = base + '/' + determine_name(objects, **_object)
						print('{} {} {filetype}'.format(object_id, name, **_object))
						try: makedirs(dirname(name))
						except: pass
						mtp.get_file_to_file(object_id, name)
		except:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

