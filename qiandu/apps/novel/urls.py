"""qiandu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include,re_path

from . import views

urlpatterns = [
    path('category_all',views.CategoryAllAPIView.as_view()),  #查询所有的小说分类
    path('category',views.CategoryAPIView.as_view()),  #小说分类查询
    path('detail',views.DetailAPIView.as_view()),  #小说详情查询
    path('chapter_list',views.DetailListAPIView.as_view()),  #小说章节查询
    path('chapter',views.ChapterContentAPIView.as_view()), #章节内
    path('novel',views.NovelAllAPIView.as_view()),
    path('bookrack',views.BookrackAPIView.as_view()),
    path('addnovel', views.AddNovelAPIView.as_view()),
    path('recently', views.RecentlyNovelAPIView.as_view()),
    path('bookrack_recently', views.RecentlyNovelListAPIView.as_view()),
    path('novel_delete',views.DeleteNovelAPIView.as_view())
]
