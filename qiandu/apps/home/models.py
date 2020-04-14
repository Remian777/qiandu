from django.db import models

# Create your models here.
class BannerFirst(models.Model):
    title = models.CharField(max_length=16,verbose_name='标题')
    link = models.CharField(max_length=64,verbose_name='链接')
    image = models.ImageField(upload_to='bannerOne',verbose_name='图片链接')
    info = models.TextField(verbose_name='轮播图简介')
    order = models.IntegerField(verbose_name='显示顺序')

    class Meta:
        verbose_name_plural='轮播图表1'


class BannerSecond(models.Model):
    title = models.CharField(max_length=16, verbose_name='标题')
    link = models.CharField(max_length=64, verbose_name='链接')
    image = models.ImageField(upload_to='bannerOne', verbose_name='图片链接')
    info = models.TextField(verbose_name='轮播图简介')
    order = models.IntegerField(verbose_name='显示顺序')

    class Meta:
        verbose_name_plural = '轮播图表2'


