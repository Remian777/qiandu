
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qichongjiagou.settings.dev')
django.setup()



from django.core.cache import cache

cache.set('name','jerry')

