from rest_framework.views import APIView
import re,os
from . import models, Serializers
from rest_framework.response import Response
from django.conf import settings
from django.core.cache import cache
from libs.tx_sms import sms_interface
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# 手机注册接口
class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_ser = Serializers.RegisterModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        user_ser.save()
        return Response({'status': 200, 'msg': '注册成功'})


# 发送短信接口
class SMSAPIView(APIView):
    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'status': 300, 'msg': '请输入正确的手机号'})
        if not re.match(
                r'^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$',
                mobile):
            return Response({'status': 301, 'msg': '手机格式不正确'})
        code = sms_interface.get_code()
        result = sms_interface.sms_interface(mobile, code, settings.SMS_EXC // 60)
        if not result:
            return Response({'status': 300, 'msg': '发送验证信息失败'})
        else:
            cache.set(f'sms_{mobile}', code, settings.SMS_EXC)
            return Response({'status': 200, 'msg': '短信发送成功'})


# 登录接口
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = Serializers.LoginModelSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)


        return Response({
            'status': 200,
            'msg': '登录成功',
            'gender': serializer.user.gender,
            'id': serializer.user.pk,
            'username': serializer.user.username,
            'token': serializer.token,
            'user_icon': str(serializer.user.user_icon)
        })


# 手机登录接口
class LoginMobileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Serializers.LoginMobileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'status': 200,
            'msg': '登录成功',
            'gender': serializer.user.gender,
            'id': serializer.user.pk,
            'username': serializer.user.username,
            'token': serializer.token,
            # 'user_icon': serializer.user_icon
        })


# 验证手机是否已经注册
class CheckRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        if not re.match(
                r'^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$',
                mobile):
            return Response({'status': 301, 'msg': '手机格式不正确'})
        if models.User.objects.filter(mobile=mobile).first():
            return Response({'status': 300, 'msg': '该手机号已经注册'})
        return Response({'status': 200, 'msg': '该手机号可以注册'})


#获取用户信息接口
class UserInfoAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self,request,*args,**kwargs):
        serializer = Serializers.UserInfoSerializer(instance=request.user,context={'request':request}).data

        return Response({'info':serializer})


#获取用户钱包信息接口
class UserPayInfoAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request,*args,**kwargs):
        serializer = Serializers.UserPayInfoSerializer(instance=request.user).data
        return Response(serializer)


