"""
    Author: Chris
    Time  : 2020/1/10 15:05
    File  : tasks.py
"""


from .celery import app


@app.task
def s(a1,a2):
    print(a1+a2)
    return a1+a2