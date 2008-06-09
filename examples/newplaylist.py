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
	print "Usage: %s <playlist name> <file ids / track ids>" % (sys.argv[0])

def main():
	if len(sys.argv) <= 2:
		usage()
		sys.exit(2)
		
	mtp = pymtp.MTP()
	mtp.connect()

	name = sys.argv[1]
	tracks = sys.argv[2:]
	metadata = pymtp.LIBMTP_Playlist()
	for track in tracks:
		metadata.append(track)

	playlist_id = mtp.create_new_playlist(name, metadata)
	print "Created new playlist with ID: %s" % (playlist_id)

	mtp.disconnect()
		
if __name__ == "__main__":
	main()
