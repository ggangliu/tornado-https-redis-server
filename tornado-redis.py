# -*- coding=utf-8

import redis

userInfos = ({'user': "0135lQ2x0NJYgj18oF2x0BjN2x05lQ20", 'msg': "你好", 'reply_msg': ''},
             {'user': "0135lQ2x0NJYgj18oF2x0BjN2x05lQ21", 'msg': "什么时候发货", 'reply_msg': ''},
             {'user': "0135lQ2x0NJYgj18oF2x0BjN2x05lQ22", 'msg': "请问在吗", 'reply_msg': ''})

userData = []
# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
pool = redis.ConnectionPool(host='111.230.107.188', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

r.flushall()
# r.set('who', 'ggangliu')  # key是"foo" value是"bar" 将键值对存入redis缓存
# print(r.get('who'))  # 取出键name对应的值
# print(type(r.get('who')))

pipe = r.pipeline() # 创建一个管道
for user in userInfos:
    user_name = user['user'].__str__()
    pipe.set(user_name + ':user', user['user'])
    pipe.set(user_name + ':msg', user['msg'])
    pipe.set(user_name + ':reply_msg', user['reply_msg'])

# pipe.incr('num')    # 如果num不存在则vaule为1，如果存在，则value自增1
pipe.execute()
r.save()


for user in r.keys('*:user'):
    user_dic = {}
    user_name = r.get(user)
    user_dic['user'] = user_name
    user_dic['msg'] = r.get(user_name + ':msg')
    user_dic['reply_msg'] = r.get(user_name + ':reply_msg')
    userData.append(user_dic)

userData = tuple(userData)
print type(userData)
print userData


def get_data_from_redis():
    pool = redis.ConnectionPool(host='111.230.107.188', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    user_data = []
    for user in r.keys('*:user'):
        user_dic = {}
        user_name = r.get(user)
        user_dic['user'] = user_name
        user_dic['msg'] = r.get(user_name + ':msg')
        user_dic['reply_msg'] = r.get(user_name + ':reply_msg')
        user_data.append(user_dic)

    user_data = tuple(user_data)
    return user_data


def write_data_to_redis(user_name, reply_msg):
    pool = redis.ConnectionPool(host='111.230.107.188', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set(user_name + ':reply_msg', reply_msg)