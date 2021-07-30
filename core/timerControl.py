# -*- coding: utf-8 -*-
# ==================================================
# 对 Timer 做以下再封装的目的是：当某个功能需要每隔一段时间被
# 执行一次的时候，不需要在回调函数里对 Timer 做重新安装启动
# ==================================================
import threading
import Recognize
from datetime import datetime

import time

def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec

def move():
    threadFunc()

def threadFunc():
    second = sleeptime(0, 0, 1)
    while 1 == 1:
        time.sleep(second)
        print(Recognize.datas)

my_thread = threading.Thread(target=threadFunc,args=())
my_thread.start()

