from django_filters.rest_framework import DjangoFilterBackend
from  rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from . import models,Serializers,Filters,pagenations
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


#获取所有的小说分类
class CategoryAllAPIView(ListAPIView):
    queryset = models.Novel_category.objects.all()
    serializer_class = Serializers.CategoryAllSerializer


#小说分类
class CategoryAPIView(APIView):
    def get(self,request,*args,**kwargs):
        nid = request.query_params.get('id')
        category_obj = models.Novel_category.objects.filter(pk=nid).first()
        if not category_obj:
            return Response({'status':'300','msg':'小说分类不存在'})
        novel_data = Serializers.NovelCategorySerializer(instance=category_obj,context={'request':request}).data
        return Response({'status':200,'data':novel_data})


#获取所有的小说
class NovelAllAPIView(ListAPIView):
    queryset = models.Novel.objects.all()
    serializer_class = Serializers.NovelAllSerializer
    #配置过滤器类
    filter_backends = [OrderingFilter,SearchFilter,DjangoFilterBackend,Filters.LimitFilter]
    #参与排序的字段
    ordering_fields = ['tuijian','dashang','dianji','jinpiao','shubi']
    #参与搜索的字段
    search_fields = ['novel_name'] #, 'detail'
    #分页器
    pagination_class = pagenations.NovelPageNumberPagination
    #参与分类的字段
    filter_class = Filters.NovelFilterSet


#小说详情
class DetailAPIView(APIView):
    authentication_classes = []
    def get(self,request,*args,**kwargs):
        nid = request.query_params.get('id')
        novel_obj = models.Novel.objects.filter(pk=nid).first()
        if not novel_obj:
            return Response({'status': '300', 'msg': '该小说不存在'})
        detail_data = Serializers.NovelDetailSerializer(instance=novel_obj,context={'request':request}).data
        return Response({'status':200,'detail_data':detail_data})


#小说章节
class DetailListAPIView(APIView):
    def get(self,request,*args,**kwargs):
        nid = request.query_params.get('id')

        novel_obj = models.Novel.objects.filter(pk=nid).first()
        if not novel_obj:
            return Response({'status':300,'msg':'该小说不存在'})

        chapter_data = Serializers.ChapterListSerializer(instance=novel_obj).data
        print(chapter_data)
        return Response({'status':200,'chapter_data':chapter_data})



#小说内容
class ChapterContentAPIView(APIView):
    def get(self,request,*args,**kwargs):
        nid = int(request.query_params.get('id'))
        cid = int(request.query_params.get('chapter_id'))
        novel_obj = models.Novel.objects.filter(pk=nid).first()
        if not novel_obj:
            return Response({'status':300,'msg':'该小说不存在'})
        Chapter_obj = models.Novel_chapter.objects.filter(pk=cid).first()
        if not Chapter_obj:
            return Response({'status': 300, 'msg': '该小说章节不存在'})

        if cid > novel_obj.chapter_end + 1:
            return Response({'status': 202, 'msg': '已经是小说的最新章节'})


        if  cid > novel_obj.chapter_end or cid < novel_obj.chapter_start :
            return Response({'status':300,'msg':'该小说章节不存在'})

        chapter_content_data = Serializers.ChapterContentSerializer(instance=Chapter_obj).data
        return Response({'status':200,'chapter_data':chapter_content_data})


#查询小说书架
class BookrackAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request,*args,**kwargs):
        novel_all = models.Novel_list.objects.filter(user=request.user).order_by('-id').all()
        novel_list = []
        for obj in novel_all:
            if obj:
                serializer = Serializers.BookrackSerializer(instance=obj).data
                novel_list.append(serializer)


        return Response(data={'bookrack':novel_list})


#添加到书架
class AddNovelAPIView(APIView):
    def get(self,request,*args,**kwargs):

        uid = request.query_params.get('user_id')
        nid = request.query_params.get('novel_id')

        # 判断最近阅读表中是否存在该小说 如果存在 直接将最近阅读表中的chapter_id赋值给书架表的chapter_id

        recently_novel_obj = models.recently_reading.objects.filter(user_id=uid,Novel_id=nid).first()
        if recently_novel_obj:
            chapter_id = recently_novel_obj.chapter_id
            recently_novel_obj.delete()
        else:
            novel_obj = models.Novel.objects.filter(pk=nid).first()
            chapter_id = novel_obj.chapter_start

        bookrack_obj = models.Novel_list.objects.filter(user_id=uid,Novel_id=nid).first()
        if bookrack_obj:
            return Response({'status': 301, 'msg': '小说已经存在书架中'})
        models.Novel_list.objects.create(user_id=uid,Novel_id=nid,chapter_id=chapter_id)
        return Response({'status':200,'msg':'加入书架成功'})


#查询已经购买的小说的章节
class SelectChapter(APIView):
    def get(self,request,*args,**kwargs):
        pass



#小说最近阅读接口
class RecentlyNovelAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self, request, *args, **kwargs):
        nid = request.data.get('novel_id')
        cid = request.data.get('chapter_id')
        novel_obj = models.Novel_list.objects.filter(Novel_id=nid, user=request.user).first()
        if novel_obj:
            print(novel_obj)
            novel_obj.chapter_id = cid
            novel_obj.save()
            return Response({'status':201,'msg':'书架ok'})
        else:
            novel_obj = models.recently_reading.objects.filter(Novel=nid,user=request.user).first()
            if not novel_obj:
                models.recently_reading.objects.create(user=request.user, Novel_id=nid, chapter_id=cid)
            else:
                novel_obj.chapter_id = cid
                novel_obj.save()
            return Response({'status': 200, 'msg': 'ok'})


#小说最近阅读查询接口
class RecentlyNovelListAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request,*args,**kwargs):
        novel_objs = models.recently_reading.objects.filter(user=request.user).order_by('-update_time').all()[:10]
        novel_list = []
        for obj in novel_objs:
            if obj:
                serializer = Serializers.RecentlyNovelListSerializer(instance=obj).data
                novel_list.append(serializer)

        return Response(data={'bookrack': novel_list})


#小说删除接口
class DeleteNovelAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request,*args,**kwargs):
        nid = request.query_params.get('nid')
        print(nid)


        novel_obj = models.Novel_list.objects.filter(user=request.user,Novel_id=nid).first()
        if novel_obj:
            print(11)
            novel_obj.delete()
            return Response({'status':200,'msg':'删除成功'})
        else:
            novel_obj = models.recently_reading.objects.filter(user=request.user,Novel_id=nid).first()
            print(222)
            novel_obj.delete()
            return Response({'status': 200, 'msg': '删除成功'})












