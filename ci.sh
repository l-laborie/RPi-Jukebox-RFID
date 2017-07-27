#!/usr/bin/env sh

# linter
pep8 jukebox
pep257 jukebox
pylint -rno jukebox

# tester
py.test -vv --cov=jukebox --cov-report=term-missing --cov-report=html --cov-report=xml jukebox
