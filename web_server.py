# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        respone = {
                   'key': 111,
                   'name': 'www',
                   'isCompleted': False
                  }
        response_body = json.dumps(respone)
        self.write(response_body.encode('utf-8'))


class TaskHandler(tornado.web.RequestHandler):
    def get(self):
        respone = {
            'key': 1114,
            'name': 'www',
            'isCompleted': False
        }
        response_body = json.dumps(respone)
        self.write(response_body.encode('utf-8'))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/task", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3001)
    tornado.ioloop.IOLoop.current().start()
