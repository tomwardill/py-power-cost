import os
import sys

sys.path.append('/var/www/sites/howrandom.net/bits/')
sys.path.append('/var/www/sites/howrandom.net/bits/py-power-cost/django')
sys.path.append('/var/www/sites/howrandom.net/bits/py-power-cost/')
sys.path.append('/var/www/sites/howrandom.net/bits/py-power-cost/web/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
