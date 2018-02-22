# -*- coding=utf-8

import redis

# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
pool = redis.ConnectionPool(host='111.230.107.188', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)


r.set('who', 'ggangliu')  # key是"foo" value是"bar" 将键值对存入redis缓存
print(r.get('who'))  # 取出键name对应的值
print(type(r.get('who')))

pipe = r.pipeline() # 创建一个管道
pipe.set('name', 'ggangliu')
pipe.set('role', 'sb')
pipe.sadd('faz', 'baz')
pipe.incr('num')    # 如果num不存在则vaule为1，如果存在，则value自增1
pipe.execute()

print(r.get("name"))
print(r.get("role"))
print(r.get("num"))