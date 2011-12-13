Refbinder overview
==================

Refbinder is a modified version of Raymond Hettinger's [Decorator for BindingConstants at compile time (Python recipe)](http://code.activestate.com/recipes/277940/) with a convenient API for mass-binding.

To enable Refbinder in a program that uses it, install Refbinder and set the
environmental variable `REFBINDER_AUTOENABLE` to `1`.


Installation
============

`python setup.py install`

This installs the module `refbinder`.


Running the tests
=================

Install Twisted, then run `trial refbinder`


Contributing
============

Patches and pull requests are welcome.

This coding standard applies: http://ludios.org/coding-standard/
