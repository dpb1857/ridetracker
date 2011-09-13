# -*- Makefile -*-


default: help

python:
	django_bootstrap.py . --infrastructure-only
	python/bin/pip install django_countries

prod_fixperms:
	sudo chown -R www-data:www-data data

prod_update:
	git pull
	(cd tracker && ../python/bin/python manage.py collectstatic)
	supervisorctl -c ../supervisor/etc/supervisord.conf restart pbpresults
	sudo rm -rf data/django_cache

help:
	@echo
	@echo "Type 'make python' to build the local virtualenv python to run this project."
	@echo
	@echo "If you need to build python for your system, you can go into the build-python"
	@echo "directory and type 'make python' as root to configure and install python in"
	@echo "/usr/local/python-<version>"
	@echo
