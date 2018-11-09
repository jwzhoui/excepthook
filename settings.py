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

# poi 缓存时间
POI_STATUS_OK_REDIS_EXPIRE = 60 * 60 * 24
POI_STATUS_FAIL_REDIS_EXPIRE = 60 * 60
# poi缓存key开头
REDIS_EXC_KEY = 'not_catch_exception'

