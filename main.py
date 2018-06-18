#-*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
#import tornado.websocket
from tornado.options import define, options
#from tornado import gen
#import time
import ssl
import os
import pprint
import json
import traceback
import importlib

cl=[]
connections={}

command = {
    "order": "exec_bash",
    "cmd_str": "ls"
}


class ConsoleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(pprint.pformat(cl))
        self.write(pprint.pformat(connections))

class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            id      = self.get_argument('id')
            cmd_str = self.get_argument('cmd_str')
            connections[id]["cn"].write_message(
                json.dumps({
                    "order": "exec_bash",
                    "cmd_str": cmd_str
                })
            )
        except tornado.web.MissingArgumentError:
            pass

if __name__ == "__main__":
# https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
    module = importlib.import_module('sample_rhizome')
    module.cl = cl
    module.connections = connections
    rhizome = getattr(module, 'WebSocketHandler')

# app
    app = tornado.web.Application([
#        (r"/websocket", WebSocketHandler),
        (r"/websocket", rhizome),
        (r"/console",   ConsoleHandler),
        (r"/command",   CommandHandler),
    ])

# options
    define("protocol",      default="wss:", help="ws: or wss:(default)")
    define("port",          default=8888, help="listening port", type=int)    
    define("data_dir",      default="/etc/letsencrypt/live/titurel.uedasoft.com/", help="cert file path for running with ssl")
    define("cert_file",     default="cert.pem", help="cert file name for running with ssl")
    define("privkey_file",  default="privkey.pem", help="privkey file name for running with ssl")
    define("config_file",   default="", help="config file path")
    options.parse_command_line()
    if options.config_file:
        options.parse_config_file(options.config_file)

    if options.protocol == "ws:":
        http_server = tornado.httpserver.HTTPServer(app)
    else:
#       app.listen(8888)
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        data_dir = options.data_dir
        ssl_ctx.load_cert_chain(os.path.join(data_dir, options.cert_file),
                                os.path.join(data_dir, options.privkey_file))
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)

    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
