# encoding: utf-8


import sys
import traceback


def hq_format_exc():
    try:
        etype, value, tb = sys.exc_info()
        err = ''.join(traceback.format_exception(etype, value, tb, None))
        # import threading
        from execepthook.redis_cache import def_inset_exc_to_redis
        def_inset_exc_to_redis(err)
        # print threading.Thread(target=def_inset_exc_to_redis, args=(err,)).start()
        # (err)
        # print 'def_inset_exc_to_redis %f'%(time.time()-d)
    finally:
        etype = value = tb = None
# 多线程 或多进程 捕捉 重写traceback的format_exc函數
traceback.hq_thread_excepthook = hq_format_exc
# 一般捕捉 定义全局异常捕获
# sys.excepthook = hq_format_exc