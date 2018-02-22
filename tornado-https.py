# -*- coding=utf-8 -*-

import os, json
from tornado.ioloop import IOLoop
from tornado import gen, web
from tornado import httpserver
from tornado import ioloop


class IndexHandler(web.RequestHandler):
    def data_received(self, chunk):
        print 'data_received: '
        print chunk

    @gen.coroutine
    def get(self):
        value = self.get_argument('echostr', 'ggangliu')
        print 'Request:'
        print self.request
        user_infos = (["0135lQ2x0NJYgj18oF2x0BjN2x05lQ20", "你好"], ["0135lQ2x0NJYgj18oF2x0BjN2x05lQ22", "多久发货"], ["0135lQ2x0NJYgj18oF2x0BjN2x05lQ23", "在吗"])
        self.render("index.html", users=user_infos)
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
        value = self.get_query_argument('echostr', 'ggangliu')
        print 'Request:'
        print self.request
        self.write(value)
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
    application = web.Application([(r"/", IndexHandler), (r"/message", CustomerServiceHandler), ], autoreload=True,  **settings)
    server = httpserver.HTTPServer(application)
    server.listen(80)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    test_main()
