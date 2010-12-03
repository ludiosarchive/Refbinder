#!/bin/sh -e

MYPY_CONSTANT_BINDER_AUTOENABLE=0 time python     -W all `which trial` mypy
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time python     -W all `which trial` mypy
MYPY_CONSTANT_BINDER_AUTOENABLE=0 time python -O  -W all `which trial` mypy
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time python -O  -W all `which trial` mypy
MYPY_CONSTANT_BINDER_AUTOENABLE=0 time python -OO -W all `which trial` mypy
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time python -OO -W all `which trial` mypy

MYPY_CONSTANT_BINDER_AUTOENABLE=0 time pypy       -W all `which trial` mypy
MYPY_CONSTANT_BINDER_AUTOENABLE=1 time pypy       -W all `which trial` mypy

#MYPY_CONSTANT_BINDER_AUTOENABLE=0 time jython      `which trial` mypy
#MYPY_CONSTANT_BINDER_AUTOENABLE=1 time jython      `which trial` mypy
