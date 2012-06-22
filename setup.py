#!/usr/bin/env python
#
# Setup.py for Pymtp
#
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
	name = "mtp",
	version = "1.0.0",
	description = "LibMTP bindings for Python",
	long_description='''
''',
	cmdclass = {'build_ext': build_ext},
	ext_modules = [Extension('mtp', ['mtp.pyx', ],
		libraries=['mtp', ],
		include_dirs=['/usr/include', ],
		extra_compile_args=['-Wno-cast-qual', '-Wno-strict-prototypes', ],
		# pyrex_gdb=True,
		)],
	author = "M. Dietrich",
	author_email = "mdt@pyneo.org",
	url = "http://pyneo.org/python-mtp/",
	# py_modules = ["mtp"],
	# data_files=[ ('share/mtp', ('mtp.py', )), ],
	)
