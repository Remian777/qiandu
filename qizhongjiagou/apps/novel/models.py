from django.db import models
from user.models import User
from django.conf import settings


def novel_detail(detail):
    if len(detail) > 150:
        return detail[:150] + '...'

    else:
        return detail

# Create your models here.
# 小说表
class Novel(models.Model):
    novel_img = models.FileField(upload_to='image/', default='image/default.jpg', verbose_name='小说图片')
    novel_status = models.IntegerField(choices=((0, '连载中'), (1, '已完结')), verbose_name='小说状态')
    novel_name = models.CharField(max_length=64, verbose_name='小说名字')
    detail = models.TextField(verbose_name='小说简介')
    tuijian = models.IntegerField(verbose_name='推荐数量', default=0)
    shubi = models.IntegerField(verbose_name='书币', default=0)
    jinpiao = models.IntegerField(verbose_name='金票', default=0)
    dashang = models.IntegerField(verbose_name='打赏数量', default=0)
    dianji = models.IntegerField(verbose_name='点击数量', default=0)
    total_words = models.IntegerField(verbose_name='总字数', default=0)
    author = models.ForeignKey(to='Author', related_name='Novel', db_constraint=False, on_delete=models.DO_NOTHING,
                               verbose_name='小说作者')  # 小说作者
    category = models.ForeignKey(to='Novel_category', related_name='novel_category', null=True, verbose_name='小说分类',
                                 db_constraint=False, on_delete=models.CASCADE)
    chapter_start = models.IntegerField(verbose_name='小说章节开始id', default=0)
    chapter_end = models.IntegerField(verbose_name='小说章节结束id', default=0)
    is_vip = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = '小说表'

    def __str__(self):
        return self.novel_name

    # 作者名字
    @property
    def author_name(self):
        return self.author.author_name

    @property
    def novel_detail(self):
        if len(self.detail) > 150:
            return self.detail[:150] + '...'

        else:
            return self.detail

    # 分类名
    @property
    def category_name(self):
        return self.category.category_name

    # 小说章节
    @property
    def chapter_list(self):
        chapter_list = []
        for i in self.Novel.all():
            chapter_list.append({
                'chapter_id': i.pk,
                'is_free': i.is_free,
                'price': i.price,
                'novel_chapter': i.novel_chapter
            })
        return chapter_list


# 作者表
class Author(models.Model):
    author_name = models.CharField(max_length=32, verbose_name='作者')
    author_gender = models.IntegerField(choices=((0, '男'), (1, '女')), default=0, verbose_name='作者性别')
    author_detail = models.TextField(verbose_name='作者简介', default='')
    author_icon = models.FileField(upload_to='icon/', default='icon/default.jpg', verbose_name='作者图片')
    author_user = models.ForeignKey(User, null=True, related_name='author', db_constraint=False,
                                    on_delete=models.DO_NOTHING, verbose_name='是否是本网站用户')

    class Meta:
        verbose_name_plural = '作者表'


# 小说分类
class Novel_category(models.Model):
    category_name = models.CharField(max_length=64, verbose_name='分类名字')
    category_file = models.FileField(upload_to='category/', default='category/default.jpg', verbose_name='分类图片')

    class Meta:
        verbose_name_plural = '小说分类表'

    @property
    def novel_list(self):
        novel_list = []
        for i in self.novel_category.all():
            novel_list.append({
                'novel_name': i.novel_name,
                'novel_img': r'media/image/' + str(i.novel_img).split('\\')[-1],
                'novel_id': i.pk,
                'novel_detail': novel_detail(i.detail),
                'novel_author': i.author.author_name,
                'novel_wroks': i.total_words,
                'novel_status': i.novel_status
            })

        return novel_list

    def __str__(self):
        return self.category_name


# 小说章节表
class Novel_chapter(models.Model):
    is_free = models.BooleanField(default=True, verbose_name='是否免费')
    price = models.IntegerField(verbose_name='价格', default=0)
    novel_chapter = models.CharField(max_length=64, verbose_name='小说章节')
    content = models.CharField(verbose_name='章节路径', max_length=255)
    words = models.IntegerField(verbose_name='字数', default=0)
    novel = models.ForeignKey(to='Novel', null=True, related_name='Novel', verbose_name='小说外键',
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '小说章节表'

    def __str__(self):
        return self.novel_chapter

    # 小说名字
    @property
    def novel_name(self):
        return self.novel.novel_name

    # 作者名字
    @property
    def author_name(self):
        return self.novel.author.author_name

    @property
    def text(self):
        text = ''
        with open(self.content, 'r', encoding='utf-8') as fr:
            for i in fr.read():
                text += i
        return text


# 评论点赞表
class Comment(models.Model):
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间
    comment_content = models.TextField()  # 评论内容
    user = models.ForeignKey(User, db_constraint=False, on_delete=models.DO_NOTHING)  # 评论用户
    Novel = models.ForeignKey(to='Novel', db_constraint=False, on_delete=models.CASCADE)  # 评论的小说
    up_number = models.IntegerField(default=0)  # 点赞数
    parent = models.ForeignKey(to='Comment', db_constraint=False, null=True, on_delete=models.DO_NOTHING)  # 子评论

    class Meta:
        verbose_name_plural = '小说评论表'


# 小说书架表
class Novel_list(models.Model):
    Novel = models.ForeignKey(to='Novel', related_name='Novel_list', null=True, db_constraint=Novel,
                              on_delete=models.DO_NOTHING, verbose_name='小说外键')
    user = models.ForeignKey(User, db_constraint=False, related_name='user', on_delete=models.DO_NOTHING,
                             verbose_name='用户外键')
    chapter = models.ForeignKey(to=Novel_chapter, null=True, related_name='chapter', db_constraint=False,
                                on_delete=models.DO_NOTHING, verbose_name='章节id')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name_plural = '小说书架表'

    def __str__(self):
        return str(self.pk)

    @property
    def novel_info(self):
        novel_dic = {}
        novel_dic['novel_name'] = self.Novel.novel_name
        novel_dic['novel_img'] = r'media/image/' + str(self.Novel.novel_img).split('\\')[-1]
        novel_dic['novel_detail'] = novel_detail(self.Novel.detail)
        novel_dic['total_words'] = self.Novel.total_words
        novel_dic['novel_status'] = self.Novel.novel_status
        novel_dic['novel_id'] = self.Novel.pk
        novel_dic['novel_author'] = self.Novel.author.author_name
        novel_dic['chapter_start'] = self.Novel.chapter_start
        novel_dic['category'] = self.Novel.category.category_name
        novel_dic['chapter_name'] = self.chapter.novel_chapter
        return novel_dic


# 普通最近阅读表
class recently_reading(models.Model):
    Novel = models.ForeignKey(to='Novel', related_name='recently', null=True, db_constraint=Novel,
                              on_delete=models.DO_NOTHING, verbose_name='小说外键')
    user = models.ForeignKey(User, db_constraint=False, related_name='recently_user', on_delete=models.DO_NOTHING,
                             verbose_name='用户外键')
    chapter = models.ForeignKey(to=Novel_chapter, null=True, related_name='recently_chapter', db_constraint=False,
                                on_delete=models.DO_NOTHING, verbose_name='章节id')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name_plural='最近阅读表'

    @property
    def novel_info(self):
        novel_dic = {}
        novel_dic['novel_name'] = self.Novel.novel_name
        novel_dic['novel_img'] = r'media/image/' + str(self.Novel.novel_img).split('\\')[-1]
        novel_dic['novel_detail'] = novel_detail( self.Novel.detail)
        novel_dic['total_words'] = self.Novel.total_words
        novel_dic['novel_status'] = self.Novel.novel_status
        novel_dic['novel_id'] = self.Novel.pk
        novel_dic['novel_author'] = self.Novel.author.author_name
        novel_dic['chapter_start'] = self.Novel.chapter_start
        novel_dic['category'] = self.Novel.category.category_name
        novel_dic['chapter_name'] = self.chapter.novel_chapter
        return novel_dic
