"""
    Author: Chris
    Time  : 2020/1/10 14:48
    File  : celery.py
"""

# celery使用

from celery import Celery



# broker 任务仓库
broker = 'redis://127.0.0.1:6379/5'
# backend 任务结果仓库
backend = 'redis://127.0.0.1:6379/6'
#include 任务(函数所在文件)


app = Celery(broker=broker,backend=backend,include=['celery_task.tasks'])