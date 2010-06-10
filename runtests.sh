#!/bin/zsh -e

time PY_OPTIMIZER_DONT_OPTIMIZE=1 python -N -W all `which trial` mypy
echo
echo "Now running with the Python test runner..."
python -N -W all -m unittest discover
