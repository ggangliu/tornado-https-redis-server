# -*- coding=utf-8 -*-

import os
import json
import redis
from tornado import gen, web
from tornado import httpserver
from tornado import ioloop

#user_infos = (["0135lQ2x0NJYgj18oF2x0BjN2x05lQ20", "你好"], ["0135lQ2x0NJYgj18oF2x0BjN2x05lQ22", "多久发货"], ["0135lQ2x0NJYgj18oF2x0BjN2x05lQ23", "在吗"])

# user_infos = ({'user': "0135lQ2x0NJYgj18oF2x0BjN2x05lQ20", 'msg': "你好", 'reply_msg': ''},
#               {'user': "0135lQ2x0NJYgj18oF2x0BjN2x05lQ21", 'msg': "什么时候发货", 'reply_msg': ''},
#               {'user': "0135lQ2x0NJYgj18oF2x0BjN2x05lQ22", 'msg': "请问在吗", 'reply_msg': ''})


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
    print user_data
    return user_data


def write_data_to_redis(user_name, reply_msg):
    pool = redis.ConnectionPool(host='111.230.107.188', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set(user_name + ':reply_msg', reply_msg)


class IndexHandler(web.RequestHandler):
    def data_received(self, chunk):
        print 'data_received: '
        print chunk

    @gen.coroutine
    def get(self):
        value = self.get_argument('echostr', 'ggangliu')
        print 'Request:'
        print self.request
        user_info = get_data_from_redis()
        self.render("index.html", users=user_info)
        #self.write(value)
        #self.on_finish()

    @gen.coroutine
    def post(self):
        print 'Post:'
        param = self.request.body.decode('utf-8')
        print json.loads(param)
        yield self.write("success")
        self.on_finish()


class CustomerServiceHandler(web.RequestHandler):
    """Handler customer message"""
    @gen.coroutine
    def get(self):
        user_name = self.get_query_argument('user', 'ggangliu')
        reply_msg = self.get_query_argument('reply_msg', 'ggangliu')
        write_data_to_redis(user_name, reply_msg)
        print 'Request:'
        print self.request
        # self.render("index.html", users=user_infos)
        self.write("\nuser: " + user_name)
        self.write("\nreply_msg: " + reply_msg)
        self.write("\n回复完成！")
        self.on_finish()

    @gen.coroutine
    def post(self):
        pass


def main():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    application = web.Application([(r"/", IndexHandler), (r"/message", CustomerServiceHandler), ], autoreload=True,  **settings)
    server = httpserver.HTTPServer(application, ssl_options={
           "certfile": os.path.join(os.path.abspath("."), "server.crt"),
           "keyfile": os.path.join(os.path.abspath("."), "server.key"),
    })
    server.listen(443)
    ioloop.IOLoop.instance().start()


def test_main():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    application = web.Application([(r"/", IndexHandler), (r"/reply_msg", CustomerServiceHandler), ], autoreload=True,  **settings)
    server = httpserver.HTTPServer(application)
    server.listen(80)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    test_main()
