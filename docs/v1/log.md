## Image Api
> 使用方式：client.logger.*(具体的方法)

### 目录
> 1. [查询日志](#查询日志)


1. ### 查询日志

    > logs(self, region_id, address, service,
             catalog,
             log_level=None,
             start_date=None,
             end_date=None,
             sort_field='timestamp',
             sort_order="asc",
             start_row=0, size=10)

    #### 方法参数
    名称 | 类型 | Required | 描述
    ---|---|---|---
    region_id | string | 是 | region id
    address | string | 是 | 容器服务：命名空间; Sundae服务：ip地址
    service | string | 是 | 服务。容器服务：pod_name/rc_name；Sundae服务：日志文件名称,如nova-api等
    catalog | string | 是 | 分类。ec/ecs/ecr
    log_level| string | 否 | 日志等级DEBUG、INFO、WARN、ERROR、FATAL
    start_date| string | 否 | 开始日期。符合%Y-%m-%d格式
    end_date| string | 否 | 结束日期。符合%Y-%m-%d格式
    sort_field| string | 否 | 排序字段。默认timestamp
    sort_order| string | 否 | 排序。asc:升序；desc降序
    start_row | int | 否 | 查询开始行。默认0
    size | int | 否 | 获取的数据行数。默认10

    ##### 示例

    > c.logger.logs("regionone", "10.16.118.102", "nova-api", catalog="ec", log_level="DEBUG",
                         start_date="2016-08-23", end_date="2016-08-25", sort_order="desc", size=2)

    ```
    {
        "hits": {
            "hits": [
                {
                    "sort": [
                        "1472145978.073"
                    ],
                    "_type": "ec",
                    "_index": "regionone_10.16.118.102_nova-api",
                    "_score": null,
                    "_source": {
                        "timestamp": "1472145978.073",
                        "message": "nova.db.sqlalchemy.api [req-8582e6da-2b6f-49d3-b3ea-2aeee1d131a4 None] ccccccccccccccccSELECT quota_classes.created_at AS quota_classes_created_at, quota_classes.updated_at AS quota_classes_updated_at, quota_classes.deleted_at AS quota_classes_deleted_at, quota_classes.deleted AS quota_classes_deleted, quota_classes.id AS quota_classes_id, quota_classes.class_name AS quota_classes_class_name, quota_classes.resource AS quota_classes_resource, quota_classes.hard_limit AS quota_classes_hard_limit \nFROM quota_classes \nWHERE quota_classes.deleted = :deleted_1",
                        "log_level": "INFO",
                        "time": "2016-08-25 17:26:18.073"
                    },
                    "_id": "AVbBBW1UKHeo-Uvmfx_b"
                },
                {
                    "sort": [
                        "1472145978.072"
                    ],
                    "_type": "ec",
                    "_index": "regionone_10.16.118.102_nova-api",
                    "_score": null,
                    "_source": {
                        "timestamp": "1472145978.072",
                        "message": "nova.db.sqlalchemy.api [req-8582e6da-2b6f-49d3-b3ea-2aeee1d131a4 None] 3333333333333False33333333337cac247114af4de9bebf82484becadd533333333333d12b0cf65d6246babc455cc993caf201333333333True",
                        "log_level": "INFO",
                        "time": "2016-08-25 17:26:18.072"
                    },
                    "_id": "AVbBBW1UKHeo-Uvmfx_Z"
                }
            ],
            "total": 2220,
            "max_score": null
        },
        "took": 22,
        "timed_out": false,
        "_shards": {
            "successful": 5,
            "failed": 0,
            "total": 5
        }
    }
    ```