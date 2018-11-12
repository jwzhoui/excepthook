## excepthook使用说明

> 1. [excepthook API](/docs/v1/log.md)
> 1. [未捕获异常告警服务参数配置](/docs/v1/fluentd-config.md)

### excepthook在python项目中的使用

```
# encoding: utf-8
# 需在导包最上层
import execepthook
import execepthook.hq_excepthook
import time
print time.time()

```