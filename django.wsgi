import os
import sys

sys.path.append('/opt')
sys.path.append('/opt/inventory')

os.environ['PYTHON_EGG_CACHE'] = '/opt/inventory/.python.egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'inventaires.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
