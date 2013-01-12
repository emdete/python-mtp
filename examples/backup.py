#!/usr/bin/env python
#
# python-mtp Demo program
# Released under the GPLv3
#
from __future__ import print_function
from mtp import MediaTransfer
from os.path import dirname
from os import makedirs
'''
This small program is intended to backup all files from your MTP capable
device. It enumerates over all given storages and retrieves all folders and
files from each. The files are stored in a directory named as the
serialnumber of the device followed by a directory name as the storage. The
directory structure below is kept as MTP exposes it.

Be aware that on most devices contacts and messages are not backed up this way.
Most Android devices have a feature to store all contacts to the storage in a
single huge vcard file (and can then backed up), messages can be stored to the
storage by apps like Message Sync (mind the space - there is another app
without, the one i used has a letter with blue/green arrows as icon) and backed
up then with this program out of the device.
'''

def determine_name(objects, name, parent_id=None, **v):
	if not parent_id:
		return name
	return determine_name(objects, **objects[parent_id]) + '/' + name

def main(root='.'):
	with MediaTransfer() as mtp:
		try:
			info = mtp.get_deviceinfo()
			#print('Backup serialnumber: "{serialnumber}"'.format(**info))
			base = root + '/' + info['serialnumber']
			for storage_id, storage in mtp.storages.items():
				#print('Backup storage: "{storage_description}"'.format(**storage))
				base = base + '/' + storage['storage_description']
				objects = mtp.objects(storage_id)
				for object_id, _object in objects.items():
					if (_object['filetype'] != 'FOLDER'
					# here you could filter files, i.e. by name:
					# and '2012-10' in _object['name']
					# and 'mp4' in _object['name']
					# or by type:
					# and _object['filetype'] == 'JPEG'
					):
						name = base + '/' + determine_name(objects, **_object)
						print('backuped: {} {} {filetype}'.format(object_id, name, **_object))
						try: makedirs(dirname(name))
						except: pass
						mtp.get_file_to_file(object_id, name)
					else:
						print('ignored: {} {} {filetype}'.format(object_id, _object.get('name', '-'), **_object))
		except object, e:
			for n in mtp.get_errorstack():
				print('{errornumber}: {error_text}'.format(**n))
			raise e

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])

