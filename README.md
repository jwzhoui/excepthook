## LogClient使用说明

> 1. [logclient API](/docs/v1/log.md)
> 1. [日志采集服务参数配置](/docs/v1/fluentd-config.md)

### RegistryClient在pastry中的使用

```
# coding: utf-8
from commons.dependency import provider, requires, resolve_future_dependencies
from logClient import client
from keystoneauth1.identity import v3
from keystoneauth1 import session
from django.conf import settings



@provider('log_client_api')
class BaseManager():
    def __init__(self):
        pass

    def create_client(self, region_name=None, **kwargs):
        args = ()
        authurl = settings.__getattr__('AUTH_URL')
        kwargs['project_id'] = kwargs.pop('workspace_id')
        auth = v3.Token(auth_url=authurl, **kwargs)
        keystonesession = session.Session(auth=auth)
        kwargs['auth'] = auth
        kwargs['session'] = keystonesession

        del kwargs['token']

        return client.Client("1", *args, **kwargs)

@provider('log_api')
class LogManager():

    def __init__(self):
        pass

    def logs(self, log_client, region_id, address, service,
             catalog,
             log_level=None,
             start_date=None,
             end_date=None,
             sort_field='timestamp',
             sort_order="asc",
             start_row=0, size=10):
        return log_client.logger.logs(region_id, address,
            service, catalog, log_level, start_date, end_date,
            sort_field, sort_order, start_row, size);

```