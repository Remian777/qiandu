from alipay import AliPay
from .settings import *

alipay = AliPay(
    #设置应用ID
    appid=APP_ID,
    app_notify_url=None,  #该通知接口一般设置None
    #应用私钥
    app_private_key_string=APP_PRIVATE_KEY_STRING,

    #阿里pay应用公钥
    alipay_public_key_string=ALIPAY_PUBLIC_KEY_STRING,

    #签名算法,采用RSA2
    sign_type=SING,

    #是否是沙箱环境
    debug=DEBUG

)