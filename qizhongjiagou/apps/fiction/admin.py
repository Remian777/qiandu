from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Fiction)
admin.site.register(models.comment)
admin.site.register(models.Fiction_tag)
admin.site.register(models.Fiction_catelog)
admin.site.register(models.Fiction_list)
admin.site.register(models.Author)
admin.site.register(models.Fction_category)
