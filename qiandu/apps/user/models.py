from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
#用户表
class User(AbstractUser):
    mobile = models.CharField(max_length=11,verbose_name='手机号',unique=True)
    user_icon = models.FileField(upload_to='user_icon/',default='user_icon/default.jpg',verbose_name='用户头像')
    gender = models.IntegerField(choices=((0,'男'),(1,'女')),default=0,verbose_name='用户性别')
    is_vip = models.CharField(default='普通会员',max_length=64)
    is_delete = models.BooleanField(default=False,verbose_name='是否注销')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    n_money = models.IntegerField(verbose_name='书币数量',default=0)
    recommend_number = models.IntegerField(verbose_name='推荐票数量',default=1)
    gold = models.IntegerField(verbose_name='金币',default=0)

    @property
    def lately_data(self):
        lately_data = []
        # print(self.user.all()[0].Novel.novel_name)
        for i in self.user.all():
            lately_data.append({
                'novel_name':i.Novel.novel_name,
                'novel_img': r'media/image/' + str(i.Novel.novel_img).split('\\')[-1],
                'novel_detail':i.Novel.detail,
                'total_words':i.Novel.total_words,
                'novel_status':i.Novel.novel_status,
                'novel_id':i.Novel.pk,
                'novel_author':i.Novel.author.author_name,
                'chapter_start':i.Novel.chapter_start,
                'category':i.Novel.category.category_name
            })
        # print(lately_data)
        return lately_data