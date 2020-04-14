import time,datetime
from rest_framework import serializers
from libs.alipay import alipay,alipay_gateway
from . import models
from django.conf import settings
from novel.models import Novel_chapter




#订单序列化类
class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ('money',)
        extra_kwargs = {
            'monery':{
                'required':True
            }
        }
    def validate(self, attrs):

        money = attrs.get('money')
        try:
            money = int(money)
        except:
            raise ValueError('支付错误')

        #计算价格
        attrs['coin'] = money * 100

        #生成订单
        order_number = int(self._get_order_no())
        attrs['user'] = self.context.get('request').user
        attrs['order_number'] = order_number
        #生成订单链接
        order_parms = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_number,
            total_amount=money,
            subject=order_number,
            return_url=settings.RETURN_URL,  # 同步回调的前台接口
            notify_url=settings.NOTIFY_URL  # 异步回调的后台接口
        )
        pay_url = alipay_gateway + order_parms
        self.pay_url = pay_url
        return attrs

    # def create(self, validated_data):
    #     order = super().create(validated_data)
    #     number = validated_data.get('coin')
    #     user = validated_data.get('user')
    #     pay_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #     payment_detail = f'用户{user.username}在{pay_time}充值了{number}书币'
    #     models.payment.objects.create(number=number,user=user,payment_detail=payment_detail)
    #     return order













    def _get_order_no(self):
        no = '%s' % time.time()
        return no.replace('.', '', 1)



#用户购买章节序列化类
class ChaterPayAPIView(serializers.ModelSerializer):
    class Meta:
        model = models.Chapterpay
        fields = ['chapter','n_monery']
        # extra_kwgras = {
        #     'n_monery':{
        #         'required':True
        #     },
        #     'chapter': {
        #         'required': True
        #     }
        # }


    # def validate_chapter(self,value):
    #     if value.is_free == False:
    #         raise serializers.ValidationError('该小说无需购买')
    #     return value
    #

    def validate(self, attrs):
        user_obj = self.context.get('request').user
        n_monery = attrs.get('n_monery')
        if user_obj.n_money < n_monery:
            raise serializers.ValidationError('书币余额不足')
        user_obj.n_money = user_obj.n_money - n_monery
        user_obj.save()
        attrs['user'] = user_obj
        return attrs







