"""
WSGI config for vms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if 'test' in os.getcwd():
    settings_file = 'vms.settings_test'
else:
    settings_file = 'vms.settings_production'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)

application = get_wsgi_application()