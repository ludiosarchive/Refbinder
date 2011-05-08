#!/usr/bin/env python

from distutils.core import setup

import mypy

setup(
	name='Mypy',
	version=mypy.__version__,
	description=("Python utilities: constant binder for performance, "
		"file cache, faster urandom, StringFragment, Constant, "
		"ReallyEqualMixin, and more."),
	url="https://github.com/ludios/Mypy",
	author="Ivan Kozik",
	author_email="ivan@ludios.org",
	classifiers=[
		'Programming Language :: Python :: 2',
		'Development Status :: 3 - Alpha',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
	],
	packages=['mypy', 'mypy.test'],
	package_data={'mypy.test': ['images/*']},
)
