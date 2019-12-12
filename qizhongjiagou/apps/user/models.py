from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


#用户表
class User(AbstractUser):
    mobile = models.IntegerField(verbose_name='手机号')
    is_vip = models.BooleanField(default=False,verbose_name='是否是vip')
    is_delete = models.BooleanField(default=False,verbose_name='是否注销')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    n_money = models.IntegerField(verbose_name='n币数量')
    recommend_number = models.IntegerField(verbose_name='推荐票数量')
