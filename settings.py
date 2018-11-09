# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# redis 相关
REDIS_NODES = [
    {'host': '118.126.117.140', 'port': 6379},
    # {'host': 'codis-hotel.haoqiao.com', 'port': 30000},
]
REDIS_PASSWORD = None
MAX_CONNECTIONS = None


# 缓存list名称
REDIS_EXC_KEY = 'not_catch_exception'

