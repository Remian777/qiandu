from django.db import models

# Create your models here.

#小说表
class Fiction(models.Model):
    ficiton = models.IntegerField(choices=((0,'连载中'),(1,'已完结')),verbose_name='小说状态')
    ficiton_name = models.CharField(max_length=64,verbose_name='小说名字')
    detail = models.TextField(verbose_name='小说简介')
    tuijian = models.IntegerField(verbose_name='推荐数量')
    dashang = models.IntegerField(verbose_name='打赏数量')
    char_number = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='小说数量(w)')
    author = models.ForeignKey(to='Author',db_constraint=False,on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(to='Fiction_tag')


    class Meta:
        verbose_name_plural='小说表'

    def __str__(self):
        return self.ficiton_name


#作者表
class Author(models.Model):
    author_name = models.CharField(max_length=32,verbose_name='作者')
    author_detail = models.TextField(verbose_name='作者简介')

    class Meta:
        verbose_name_plural='作者表'


#小说分类
class Fction_category(models.Model):
    category_name = models.CharField(max_length=64,verbose_name='分类名字')
    class Meta:
        verbose_name_plural='小说分类表'


    def __str__(self):
        return self.category_name



#小说章节表
class Fiction_catelog(models.Model):
    fiction_catelog = models.CharField(max_length=64,verbose_name='小说章节')
    centent = models.TextField(verbose_name='章节内容')
    fction = models.ForeignKey(to='Fiction',null=True,verbose_name='小说外键',on_delete=models.CASCADE)
    category = models.ForeignKey(to='Fction_category',null=True,verbose_name='小说分类',db_constraint=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='小说章节表'


#评论点赞表


#小说标签表
class Fiction_tag(models.Model):
    tag = models.CharField(max_length=32,verbose_name='标签名')

    class Meta:
        verbose_name_plural='小说标签表'

    def __str__(self):
        return self.tag







