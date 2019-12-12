from django.db import models

from user.models import User

#支付表
class Order(models.Model):
    order_number = models.IntegerField(verbose_name='订单号')  #订单号
    pay_way = models.IntegerField(choices=((0,'支付宝'),(1,'微信')))   # 支付方式
    create_time = models.DateTimeField(auto_now_add=True)   #创建时间
    pey_status = models.IntegerField(((0,'未支付'),(1,'支付成功')))   #支付状态
    user = models.ForeignKey(to='User',db_constraint=False,on_delete=models.DO_NOTHING)



#充值列表
