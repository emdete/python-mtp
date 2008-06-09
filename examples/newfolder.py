#!/usr/bin/env python
#
# PyMTP demo scripts
# (c) 2008 Nick Devito
# Released under the GPL v3 or later.
#

import sys
sys.path.insert(0, "../")

import pymtp

def usage():
	print "Usage: %s <folder name> <parent>\n(The parent id can be 0 for the root directory)" % (sys.argv[0])

def main():
	if len(sys.argv) <= 1:
		usage()
		sys.exit(2)
		
	mtp = pymtp.MTP()
	mtp.connect()

	name = sys.argv[1]
	parent = int(sys.argv[2])

	folder_id = mtp.create_folder(name, parent)
	print "Created new folder with ID: %s" % (folder_id)
	mtp.disconnect()
		
if __name__ == "__main__":
	main()
