from rest_framework import serializers
from . import models



#获取所有的小说分类
class CategoryAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Novel_category
        fields = ['pk','category_name']

#小说分类序
class NovelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Novel_category
        fields = ['category_name','novel_list']

#获取所有小说
class NovelAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Novel
        fields = [
            'id',
            'novel_img',
            'novel_status',
            'novel_name',
            'novel_detail',
            'tuijian',
            'shubi',
            'jinpiao',
            'dashang',
            'dianji',
            'total_words',
            'author_name',
            'category',
            'category_name',
            'is_vip',
            'chapter_start',
            'chapter_end'
        ]

#小说详情
class NovelDetailSerializer(serializers.ModelSerializer):
    novel_detail = serializers.CharField()
    class Meta:
        model = models.Novel
        fields = [
            'id',
            'novel_name',
            'novel_img',
            'novel_status',
            'novel_detail',
            'tuijian',
            'jinpiao',
            'shubi',
            'dashang',
            'dianji',
            'total_words',
            'author_name',
            'category_name',
            'chapter_start'
        ]

#小说章节
class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Novel
        fields = ['pk','novel_name','category_name','chapter_list','chapter_end','chapter_start']

#小说章节内容
class ChapterContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Novel_chapter
        fields = ['novel_name','author_name','novel_chapter','words','text']

#小说书架
class BookrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Novel_list
        fields = ['chapter','novel_info']

#最近阅读
class RecentlyNovelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.recently_reading
        fields = ['chapter', 'novel_info']