#-*- coding:utf-8 -*-
# Copy Right Takeyuki UEDA  © 2018 - All rights reserved.

import tornado.ioloop
import tornado.web
from tornado.options import define, options
import ssl
import os
import sys
import pprint
import traceback
import importlib

command = {
    "order": "exec_bash",
    "cmd_str": "ls"
}

def get_rhizosphereHandler(modulename):
    global connections
    mod = importlib.import_module(modulename)
    mod.connections = connections
    return getattr(mod, "RhizoSphereHandler")

def append_rshandler(requesthandlers, handler):
    mod = importlib.import_module(handler)

    connections={}
    mod.connections = connections

    if getattr(mod, "type") == "RS_cdpair_and_connections_shares":
        mod_clt = getattr(mod, "RS_ClientHandler")
        requesthandlers.append((mod_clt.route, mod_clt))

        mod_dev = getattr(mod, "RS_DeviceHandler")
        requesthandlers.append((mod_dev.route, mod_dev))

        connections_shares = getattr(mod, "connections_shares")
        for handler_class_name in connections_shares:
            mod_handler = getattr(mod, handler_class_name)
            requesthandlers.append((mod_handler.route, mod_handler))

    else:
        mod_gen = getattr(mod, "RS_GeneralHandler")
        requesthandlers.append((mod_gen.route, mod_gen))
    return requesthandlers

if __name__ == "__main__":
# options
    define("protocol",              default="wss:", help="ws: or wss:(default)")
    define("port",                  default=8888, help="listening port", type=int)    
    define("data_dir",              default="", help="cert file path for running with ssl")
    define("cert_file",             default="cert.pem", help="cert file name for running with ssl")
    define("privkey_file",          default="privkey.pem", help="privkey file name for running with ssl")
    define("config_file",           default="",         help="config file path")
    define("rhizosperehandlers",    default="",         help="list of handlers",multiple=True, metavar="handler1, handler2...")
    define("additional_module_path",default="",         help="path of importing modules",multiple=True, metavar="path1, path2...")
    define("static_path",           default="sample_handlers/static",        help="[mandatory] handler class name of rhizome")
    define("templates_path",        default="sample_handlers/templates",     help="[mandatory] handler class name of rhizome")

    options.parse_command_line()
    if options.config_file:
        options.parse_config_file(options.config_file)
    elif os.path.exists('./config.py'):
        options.parse_config_file('./config.py')

    print(options.additional_module_path)
    print(options.rhizosperehandlers)

# https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
    if options.additional_module_path:
        [sys.path.append(x) for x in options.additional_module_path]

# app
    requesthandlers = []

    for handler in options.rhizosperehandlers:
        requesthandlers = append_rshandler(requesthandlers, handler)


    BASE_DIR = os.path.dirname(__file__)
    app = tornado.web.Application(
        requesthandlers, 
        template_path=os.path.join(BASE_DIR, options.templates_path),
        static_path=os.path.join(BASE_DIR, options.static_path),
    )

    if options.protocol == "ws:":
        http_server = tornado.httpserver.HTTPServer(app)
    else:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        data_dir = options.data_dir
        ssl_ctx.load_cert_chain(os.path.join(data_dir, options.cert_file),
                                os.path.join(data_dir, options.privkey_file))
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)

    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()