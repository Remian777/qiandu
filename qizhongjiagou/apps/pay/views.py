from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import Serializers
from novel import models as n_models



# 订单视图类
class PayAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = Serializers.PaySerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.pay_url)
        return Response(serializer.pay_url)




#用户购买章节类
class ChapterAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request,*args,**kwargs):
        serializer = Serializers.ChaterPayAPIView(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status':200,'msg':'购买成功'})






#用户打赏书币
class PayRecommendedAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request,*args,**kwargs):
        print(request.data)
        # try:
        if request.user.recommend_number < int(request.data.get('tuijian')):
            return Response({'status': 300, 'msg': '推荐票不足'})
        else:
            request.user.recommend_number = request.user.recommend_number - int(request.data.get('tuijian'))
            request.user.save()
            novel_obj = n_models.Novel.objects.filter(pk=request.data.get('novel_id')).first()
            if novel_obj:
                novel_obj.tuijian = novel_obj.tuijian +  request.data.get('tuijian')
                novel_obj.save()
                return Response({'status':200,'msg':'打赏成功'})
            else:
                return Response({'status': 300, 'msg': '小说不存在'})

        # except:
        #     return Response({'status':300,'msg':'打赏错误'})


class PayGoldAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        print(request.data)
        if request.user.gold < int(request.data.get('jinbi')):
            return Response({'status': 300, 'msg': '金币'})
        else:
            request.user.gold = request.user.gold - int(request.data.get('jinbi'))
            request.user.save()
            novel_obj = n_models.Novel.objects.filter(pk=request.data.get('novel_id')).first()
            if novel_obj:
                novel_obj.jinpiao = novel_obj.jinpiao  + request.data.get('jinbi')
                novel_obj.save()
                return Response({'status': 200, 'msg': '打赏成功'})
            else:
                return Response({'status': 300, 'msg': '小说不存在'})
