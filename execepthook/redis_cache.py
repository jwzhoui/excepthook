# encoding: utf-8
import sys
import redis

class RedisCache(object):
    __instance = None
    _instance = None
    __REDIS_HOST = '118.126.117.140'
    __REDIS_PORT = 6379
    __EXC_KEY = 'not_catch_exception'

    @staticmethod
    def create_pool(self):
        redis_config = self.redis_nodes[0]
        redis_config['password'] = self.password
        redis_config['max_connections'] = self.max_connections
        RedisCache.pool = redis.ConnectionPool(
            **redis_config
        )

    def __new__(cls, *args, **kwargs):

        if cls.__instance == None:
            cls.__EXC_KEY = kwargs.get('__EXC_KEY','not_catch_exception')
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, __REDIS_HOST=None,__REDIS_PORT=None):
        self.redis_nodes = [
            {'host': __REDIS_HOST, 'port': __REDIS_PORT},
            # {'host': 'codis-hotel.haoqiao.com', 'port': 30000},
        ]
        self.password = None
        self.max_connections = None
        try:
            if not hasattr(RedisCache, 'pool'):
                RedisCache.create_pool(self)
            self._connection = redis.Redis(connection_pool=RedisCache.pool)

        except Exception, e:
            pass

    @classmethod
    def get_connection(cls):
        """
        #获取链接
        """

        return RedisCache(cls.__REDIS_HOST,cls.__REDIS_PORT)._connection

    @classmethod
    def inset_exc_to_redis(cls,err):
        """
        #获取链接
        """
        # print 'classmethod inset_exc_to_redis'
        # time.sleep(5)
        __EXC_KEY = cls.__EXC_KEY
        # print 'exc_key'+__EXC_KEY,err
        return cls.get_connection().lpush(__EXC_KEY,err)

def hq_thread_inset(err):
    print 'hq_thread_inset'
    RedisCache.inset_exc_to_redis(err)


def def_inset_exc_to_redis(err):
    RedisCache.inset_exc_to_redis(err)
