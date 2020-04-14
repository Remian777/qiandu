import xadmin
# Register your models here.

from . import models

xadmin.site.register(models.Novel)
xadmin.site.register(models.Comment)
xadmin.site.register(models.Novel_category)
xadmin.site.register(models.Novel_list)
xadmin.site.register(models.Author)
xadmin.site.register(models.Novel_chapter)
