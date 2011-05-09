#!/usr/bin/env python

from distutils.core import setup

import refbinder

setup(
	name='Refbinder',
	version=refbinder.__version__,
	description=('Modified version of "Decorator for BindingConstants '
		'at compile time" with a mass-binder')
	url="https://github.com/ludios/Refbinder",
	author="Ivan Kozik",
	author_email="ivan@ludios.org",
	classifiers=[
		'Programming Language :: Python :: 2',
		'Development Status :: 4 - Beta',
		'Operating System :: OS Independent',
		'Intended Audience :: Developers',
	],
	packages=['refbinder'],
)
