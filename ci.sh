#!/usr/bin/env sh

# linter
echo "pep 8"
pep8 jukebox
echo "pep 257"
pep257 jukebox
echo "pylint"
pylint -rno jukebox

# tester
py.test -vv --cov=jukebox --cov-report=term-missing --cov-report=html --cov-report=xml jukebox
