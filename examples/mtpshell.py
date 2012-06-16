#!/usr/bin/env python
#
# A PyMTP Shell - Automagically initiates the MTP device, makes it
# easier to develop and test stuff.
# (C) 2008 Nick Devito
#
from __future__ import print_function
from os import environ
from pymtp import MTP

def callback(sent, total):
	print("Sent: {}; Total: {}".format(sent, total))

def main():
	if 'LIBMTP_DEBUG' in environ: MTP.set_debug(int(environ['LIBMTP_DEBUG']))
	with MTP(False) as mtp:
		print("Welcome to the PyMTP Shell")
		print("You are currently connected to '{}'".format(mtp.get_devicename()))
		print("Your MTP object is '{}'".format("mtp"))
		print("Your progress callback object is '{}'".format("callback"))
		print("To exit, type 'quit'")
		while True:
			try:
				if mtp.device:
					result = raw_input("(connected) >>> ")
				else:
					result = raw_input("(disconnected) >>> ")
				if result.startswith("quit"):
					mtp.disconnect()
					sys.exit()
				else:
					exec result
			except Exception, message:
				print("An exception occurred: {}".format(message))

if __name__ == "__main__":
	from sys import argv
	main(*argv[1:])

