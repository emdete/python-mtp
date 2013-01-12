python-mtp
==========

python wrapper around libmtp to talk the media transfer protocol

About
-----

python-mtp is a wrapper for libmtp, allowing python applications to communicate
with all MTP devices that are supported by libmtp. For supported & tested
devices see there. It is implemented using cython.

Simple test scripts can be found in examples/ for all major operations.

Usage
-----

The wrapper makes use of the with statement and can be used as simple as:

	from mtp import MediaTransfer
	with MediaTransfer() as mtp:
		print('Infos: {}'.format(mtp.get_deviceinfo())

The examples include a simple backup script that copies all files reachable by
MTP from the device to the local directory creating a backup directory named
after the serialnumber of the device.

Tools
-----

	- backup: there is a script in the examples/ section that implemtns a
	  backup of your mtp-capable device

	- playlist: 

Major Pitfalls
--------------

libmtp has a big drawback that is a cache filled at startup. This takes alot of
time due to usb communication. Depending on the number of files it takes a
minute or more. A flag was given to the MediaTransfer-class construtor that
allows creating a connection without caching. This renders some functions
unusual, others require this mode.

On Andriod devices MTP sometimes doesn't not work if USB-debugging is enabled.

If the screenlock is active MTP is known not to work well on some devices.

Some devices have problems if you wait too long with the connect after plugging
in.

While libmtp provides errorcodes some functions just return -1 (which is not a
listed error). Other functions return a pointer and have no way to determine
the cause of the error (they just return NULL).

If you for example upload a file to a location / name that already exists you
get no explicit error code but often just a -1.

Setting the debugging level is of some help (LIBMTP\_DEBUG=255)

Some files doesn't seem to be "Media" and are not shown via mtp (for me .gpx
files did not apear).

