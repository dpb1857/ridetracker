# -*- Makefile -*-


default: help

python:
	django_bootstrap.py . --infrastructure-only
	python/bin/pip install django_countries

help:
	@echo
	@echo "Type 'make python' to build the local virtualenv python to run this project."
	@echo 
	@echo "If you need to build python for your system, you can go into the build-python"
	@echo "directory and type 'make python' as root to configure and install python in"
	@echo "/usr/local/python-<version>"
	@echo
