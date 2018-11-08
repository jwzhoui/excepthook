# encoding: utf-8
#   Copyright 2012 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import pbr.version

from execepthook import api_versions


__version__ = pbr.version.VersionInfo('python-execepthook').version_string()

API_MIN_VERSION = api_versions.APIVersion("1.0")
# The max version should be the latest version that is supported in the client,
# not necessarily the latest that the server can provide. This is only bumped
# when client supported the max version, and bumped sequentially, otherwise
# the client may break due to server side new version may include some
# backward incompatible change.
API_MAX_VERSION = api_versions.APIVersion("1.0")



import sys
import time
import traceback


def hq_format_exc():
    """Like print_exc() but return a string."""
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