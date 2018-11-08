# Fluentd参数配置
## Fluentd安装

> 1. 下载Fluentd [http://packages.treasuredata.com.s3.amazonaws.com/2/ubuntu/trusty/pool/contrib/t/td-agent/td-agent_2.3.2-0_amd64.deb](http://packages.treasuredata.com.s3.amazonaws.com/2/ubuntu/trusty/pool/contrib/t/td-agent/td-agent_2.3.2-0_amd64.deb)
> 1. 安装Fluentd `dpkg -i td-agent_2.3.2-0_amd64.deb`

## fluentd安装注意事项
1. 修改/etc/init.d/td-agent，使用root权限运行

    > TD_AGENT_USER=td-agent --> TD_AGENT_USER=root  
    > TD_AGENT_GROUP=td-agent --> TD_AGENT_GROUP=root
    
1. 安装fluentd的elasticsearch插件

    > td-agent-gem install fluent-plugin-elasticsearch
    
1. 配置td-agent参数

    > 见[配置](#配置)

1. 重启td-agent服务

    > service td-agent restart
    
## 配置
> 1. [Sundae日志参数配置](#sundae日志参数配置)
> 1. [Container日志参数配置](#container日志参数配置)
> 1. [kubernetes日志参数配置](#kubernetes日志参数配置)

## Sundae日志参数配置
```
<filter elasticsearch.sundae.service.**>
    @type record_transformer
    enable_ruby
    <record>
      timestamp ${DateTime.strptime(record['time'], "%Y-%m-%d %H:%M:%S.%N").to_time.to_f}
      log_level ${record['log_level'].upcase}
    </record>
</filter>
<filter elasticsearch.sundae.mcollective.**>
    @type record_transformer
    enable_ruby
    <record>
      timestamp ${DateTime.strptime(record['time'], "%Y-%m-%dT%H:%M:%S.%N").to_time.to_f}
      log_level ${record['log_level'].upcase}
    </record>
</filter>

<match elasticsearch.sundae.**>
  @type elasticsearch_dynamic
  host localhost
  port 9200
  index_name RegionOne_10.16.118.102_${tag_parts[-2]}
  type_name  sundae
  flush_interval 5
</match>

<source>
    @type tail
    keep_time_key true
    time_key time
    format /^D, \[(?<time>\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2}.\d{1,6}) \#[0-9]+\] (?<log_level>[A-Z]+) -- : (?<message>.*)$/
    path /var/log/mcollective.log
    pos_file /var/run/td-agent/td-agent.pos
    time_format %Y-%m-%dT%H:%M:%S.%N
    refresh_interval 2s
    tag elasticsearch.sundae.mcollective.*
  </source>
  <source>
    @type tail
    format multiline
    format_firstline /^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,3}/
    format1 /^(?<time>\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,3}) \d{1,6} (?<log_level>[A-Z]+) (?<message>.*)/
    path /var/log/nova/*.log,/var/log/glance/*.log,/var/log/cinder/*.log,/var/log/keystone/*.log,/var/log/neutron/*.log
    pos_file /var/run/td-agent/td-agent.pos
    time_format %Y-%m-%d %H:%M:%S.%N
    keep_time_key true
    time_key time
    refresh_interval 2s
    tag elasticsearch.sundae.service.*
  </source>
```

## Container日志参数配置
```
  <filter elasticsearch.container.**>
    @type record_transformer
    enable_ruby
    <record>
      timestamp ${DateTime.strptime(record['time'], "%Y-%m-%dT%H:%M:%S.%N%Z").to_time.to_f}
      log_level ${Hash("stdout"=>"INFO", "stderr"=>"ERROR")[record["stream"]]}
      message ${record['log']}
    </record>
    remove_keys log,stream
  </filter>
  <match elasticsearch.container.**>
    @type elasticsearch_dynamic
    host 10.16.115.12
    port 9200
    index_name RegionOne_${tag_parts[-2].split("_")[1]}_${tag_parts[-2].split("_")[0][0..-7]}
    type_name ecs
    flush_interval 5
  </match>
  <source>
    @type tail
    keep_time_key true
    format json
    path /var/log/containers/*.log
    pos_file /var/run/td-agent/td-agent.pos
    time_format %Y-%m-%dT%H:%M:%S.%N%Z
    refresh_interval 2s
    tag elasticsearch.container.*
  </source>
```
## kubernetes日志参数配置
```
<filter elasticsearch.kubenetes.kubenet.**>
    @type record_transformer
    enable_ruby
    <record>
      log_level ${Hash("I"=>"INFO", "E"=>"ERROR","W"=>"WARNING","D"=>"DEBUG")[record["log_level"][0]]}
      timestamp ${DateTime.strptime(Time.new.year.to_s  + '-' + Time.new.month.to_s + '-' + Time.new.day.to_s + ' ' + record['time'], "%Y-%m-%d %H:%M:%S.%N").to_time.to_f}
      message ${record['message']}
    </record>
  </filter>

 <filter elasticsearch.kubenetes.etcd.**>
    @type record_transformer
    enable_ruby
    <record>
      log_level ${Hash("I"=>"INFO", "E"=>"ERROR","W"=>"WARNING","D"=>"DEBUG")[record["log_level"]]}
      timestamp ${DateTime.strptime(record['time'], "%Y-%m-%d %H:%M:%S.%N").to_time.to_f}
      message ${record['message']}
    </record>
  </filter>

  <match elasticsearch.kubenetes.**>
    @type elasticsearch_dynamic
    host 10.156.129.49
    port 19000
    index_name 92d6075dc54747c58db9fd0f6057cbf6_10.156.129.49_${tag_parts[-2]}
    type_name ecr
    flush_interval 5
  </match>
  <source>
    @type tail
    format multiline
    format1 /^(?<log_level>[IDWE]\d{4}) (?<time>\d{1,2}:\d{1,2}:\d{1,2}.\d{1,6}) (?<message>.*)/
    keep_time_key true
    path /var/log/upstart/kube-scheduler.log,/var/log/upstart/kube-controller-manager.log,/var/log/upstart/kube-apiserver.log,/var/log/upstart/flanneld.log,/var/log/upstart/kube-proxy.log,/var/log/upstart/kubelet.log
    pos_file /var/run/td-agent/td-agent.pos
    refresh_interval 2s
    tag elasticsearch.kubenetes.kubenet.*
  </source>

  <source>
    @type tail
    format multiline
    format1 /^(?<time>\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,6}) (?<log_level>[IDWE]) (?<message>.*)/
    keep_time_key true
    path /var/log/upstart/etcd.log
    pos_file /var/run/td-agent/td-agent.pos
    refresh_interval 2s
    tag elasticsearch.kubenetes.etcd.*
  </source>
  ```