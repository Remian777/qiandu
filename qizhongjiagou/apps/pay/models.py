from django.db import models

from user.models import User

#支付表
class Order(models.Model):
    order_number = models.IntegerField(verbose_name='订单号')  #订单号
    pay_way = models.IntegerField(choices=((0,'支付宝'),(1,'微信')),verbose_name='支付方式')   # 支付方式
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='订单创建时间')   #创建时间
    pey_status = models.IntegerField(choices=((0,'未支付'),(1,'支付成功')),verbose_name='支付状态')   #支付状态
    coin = models.IntegerField(verbose_name='书币数量',null=True)
    money = models.DecimalField(max_digits=11,decimal_places=2,verbose_name='支付总额',null=True)
    user = models.ForeignKey(User,related_name='order',db_constraint=False,on_delete=models.DO_NOTHING,verbose_name='用户')


    class Meta:
        verbose_name_plural='订单表'



#消费表
class payment(models.Model):
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='消费时间')
    number = models.IntegerField(verbose_name='书币数量')
    payment_detail = models.CharField(max_length=64,verbose_name='消费详情')
    user = models.ForeignKey(to=User,db_constraint=False,related_name='payment',on_delete=models.DO_NOTHING,verbose_name='消费用户')

    class Meta:
        verbose_name_plural='消费表'





