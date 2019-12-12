"""
    Author: Chris
    Time  : 2019/12/12 19:06
    File  : test.py
"""

import os,sys,django

from qizhongjiagou.settings import dev

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qizhongjiagou.settings.dev")
django.setup()
print(dev.BASE_DIR)

print(sys.path)

