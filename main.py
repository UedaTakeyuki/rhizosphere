#-*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
#import tornado.websocket
from tornado.options import define, options
#from tornado import gen
#import time
import ssl
import os
import sys
# import pprint
# import json
import traceback
import importlib

cl=[]
connections={}
a=[]

command = {
    "order": "exec_bash",
    "cmd_str": "ls"
}


if __name__ == "__main__":
# options
    define("protocol",              default="wss:", help="ws: or wss:(default)")
    define("port",                  default=8888, help="listening port", type=int)    
    define("data_dir",              default="/etc/letsencrypt/live/titurel.uedasoft.com/", help="cert file path for running with ssl")
    define("cert_file",             default="cert.pem", help="cert file name for running with ssl")
    define("privkey_file",          default="privkey.pem", help="privkey file name for running with ssl")
    define("config_file",           default="",         help="config file path")
    define("rhizome_route",         default="/rhizome", help="route of rhizome")
    define("rhizome_module_name",   default="",         help="[mandatory] module name of rhizome")
    define("rhizome_module_path",   default="",         help="full path of rhizome module file")
    define("rhizome_handler",       default="",         help="[mandatory] handler class name of rhizome")
    options.parse_command_line()
    if options.config_file:
        options.parse_config_file(options.config_file)
    elif os.path.exists('./config.py'):
        options.parse_config_file('./config.py')


# https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
    if options.rhizome_module_path:
        sys.path.append(options.rhizome_module_path)
    module = importlib.import_module(options.rhizome_module_name)
    module.cl = cl
    module.connections = connections
    rhizome = getattr(module, options.rhizome_handler)

    module = importlib.import_module("sample_consolehandler")
    module.cl = cl
    module.connections = connections
    consolehandler = getattr(module, "ConsoleHandler")

    module = importlib.import_module("sample_commandhandler")
    module.cl = cl
    module.connections = connections
    commandhandler = getattr(module, "CommandHandler")


# app
    app = tornado.web.Application([
#        (r"/websocket", WebSocketHandler),
#        (r"/websocket", rhizome),
        (options.rhizome_route, rhizome),
        (r"/console",   consolehandler),
        (r"/command",   commandhandler),
    ])

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
