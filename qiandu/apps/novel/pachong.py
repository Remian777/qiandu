import os
import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qiandu.settings.dev")
django.setup()
from novel import models
from settings import dev


class Requ():
    def __init__(self, url, category):
        self.url = url
        self.category = category
        self.chapter_list = []
        self.category_num = 0
        self.all_count = 0
        response = requests.get(self.url)
        context = response.content.decode('utf8')
        soup = BeautifulSoup(context, 'lxml')
        self.soup = soup

    def request_novel(self):
        self.get_message()
        # self.save_novel()
        chapter = self.soup.find_all('dd')
        for index, i in enumerate(chapter):
            name = i.get_text()
            print(name)

            link = i.a["href"]
            link = 'http://www.xbiquge.la' + link
            response = requests.get(link)

            response.encoding = response.apparent_encoding

            context = response.content

            soup = BeautifulSoup(context, 'lxml')
            content = soup.prettify().split('<div id="content">')[-1]

            content = content.split('<p>')[0]
            self.content = content.replace(' ', '').replace('<br/>', '')
            self.num = len(content)
            self.category_num += 1
            try:
                chapter_path = os.path.join(self.novel_path, f'{name}.txt')
                with open(chapter_path, 'w', encoding='utf-8') as fw:
                    for i in content:
                        fw.write(i)
            except Exception as e:
                print(e)

            if index <= 300:

                # 存储章节数据
                chapter_obj = models.Novel_chapter.objects.create(
                    is_free=0,
                    novel_chapter=name,
                    content=chapter_path,
                    words=self.num,
                    novel=self.novel
                )


            else:
                chapter_obj = models.Novel_chapter.objects.create(
                    is_free=1,
                    price=300,
                    novel_chapter=name,
                    content=chapter_path,
                    words=self.num,
                    novel=self.novel

                )
            if index == 0:
                self.novel.capter_start = chapter_obj.pk
                self.novel.save()

            if index == 30:
                self.novel.capter_end = chapter_obj.pk
                self.novel.save()
                break

            self.chapter_list.append(chapter_obj)
            self.all_count += self.num
            if len(self.chapter_list) > 100:
                # self.save_chapter()
                self.chapter_list.clear()
        if self.chapter_list:
            self.save_chapter()
        self.end()

    def save_novel(self):
        # 建立分类目录
        category_path = os.path.join(dev.NOVEL_PATH, self.category)
        if not os.path.isdir(category_path):
            os.mkdir(category_path)
        # 创建分类
        self.category_obj = models.Novel_category.objects.filter(category_name=self.category).first()
        if not self.category_obj:
            self.category_obj = models.Novel_category.objects.create(category_name=self.category)
        novel_path = os.path.join(category_path, self.name)
        if not os.path.isdir(novel_path):
            os.mkdir(novel_path)
            self.novel_path = novel_path

        # 创建作者
        author_obj = models.Author.objects.create(author_name=self.author)

        # 创建小说
        self.novel = models.Novel.objects.create(
            novel_img=self.save_image(),
            novel_name=self.name,
            novel_status=0,
            detail=self.intro,
            author=author_obj,
            category=self.category_obj
        )

    def save_chapter(self):
        pass
        # models.NovelChapter.objects.bulk_create(self.chapter_list)

    def get_message(self):
        # 小说信息
        info = self.soup.select('div#info')[0]
        self.name = info.h1.get_text()
        # 作者
        self.author = info.p.get_text().split('：')[-1]
        # 小说简介
        intro = self.soup.select('div#intro')[0]
        self.intro = intro.p.next_sibling.next_sibling.get_text()
        # 小说图片
        image = self.soup.select('div#fmimg')[0]
        img_url = image.img['src']
        response = requests.get(img_url)
        self.image_response = response

    def save_image(self):
        img_path = os.path.join(dev.BASE_DIR, 'media', 'image', f'{self.name}.jpg')

        with open(img_path, 'wb') as f:
            f.write(self.image_response.content)
        return img_path

    def end(self):
        print(self.all_count)
        self.novel.total_words = self.all_count

        # self.novel.save()


response = requests.get('http://www.xbiquge.la/paihangbang/')
#
#
context = response.content.decode('utf8')
#
soup = BeautifulSoup(context, 'lxml')
#
lis = soup.find_all('div', attrs={'class': 'b3'})[1]

u = BeautifulSoup(str(lis), 'lxml')

a_l = u.find_all('ul')[0]




ulis = a_l.find_all('li')
url_list = []

for i in ulis:
    url_list.append(i.a.attrs['href'])

print(url_list)

for i in url_list[1:]:
    obj = Requ('http://www.xbiquge.la/33/33012/','完本小说')
    obj.request_novel()
