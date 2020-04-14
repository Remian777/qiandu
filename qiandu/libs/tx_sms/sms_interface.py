from .sms_settings import *
from utils.logging import logger
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
ssender = SmsSingleSender(appid, appkey)

def sms_interface(phone,code,exc):
    try:
        response = ssender.send_with_param(
            86,
            phone,
            template_id,
            params=(code,exc),
            sign=sms_sign,
            extend="", ext="")
        if response and response.get('result') == 0:
            return True
        msg = response.get('result')

    except Exception as msg:
        pass
    logger.error(f'短信发送失败 sms_{msg}')
    return False

import random
def get_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0,9))
    return int(code)