from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


#用户表
class User(AbstractUser):
    mobile = models.IntegerField(verbose_name='手机号',unique=True,default=True)
    user_icon = models.FileField(upload_to='user_icon/',default='user_icon/default.jpg',verbose_name='用户头像')
    gender = models.IntegerField(choices=((0,'男'),(1,'女')),default=0,verbose_name='用户性别')
    is_vip = models.BooleanField(default=False,verbose_name='是否是vip')
    is_delete = models.BooleanField(default=False,verbose_name='是否注销')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    n_money = models.IntegerField(verbose_name='书币数量',default=0)
    recommend_number = models.IntegerField(verbose_name='推荐票数量',default=1)
    gold = models.IntegerField(verbose_name='金币',default=0)
