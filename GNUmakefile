# -*- Makefile -*-


default: help

python:
	./util/django_bootstrap.py . --infrastructure-only
	python/bin/pip install django_countries==1.0.5

prod_fixperms:
	sudo chown -R www-data:www-data data

prod_clearcache:
	sudo rm -rf data/django_cache

prod_update:
	git pull
	(cd tracker && ../python/bin/python manage.py collectstatic)
	(cd tracker && find . -name \*.pyc -print|xargs rm -f)
	supervisorctl -c ../supervisor/etc/supervisord.conf stop pbpresults
	sudo rm -rf data/django_cache
	$(MAKE) prod_fixperms
	supervisorctl -c ../supervisor/etc/supervisord.conf start pbpresults

prod_restart:
	supervisorctl -c ../supervisor/etc/supervisord.conf stop pbpresults
	sudo rm -rf data/django_cache
	supervisorctl -c ../supervisor/etc/supervisord.conf start pbpresults

help:
	@echo
	@echo "Type 'make python' to build the local virtualenv python to run this project."
	@echo
	@echo "If you need to build python for your system, you can go into the build-python"
	@echo "directory and type 'make python' as root to configure and install python in"
	@echo "/usr/local/python-<version>"
	@echo
