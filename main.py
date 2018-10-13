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
import pprint
# import json
import traceback
import importlib

#cl=[]
connections={}
#a=[]

command = {
    "order": "exec_bash",
    "cmd_str": "ls"
}


if __name__ == "__main__":
# options
    define("protocol",              default="wss:", help="ws: or wss:(default)")
    define("port",                  default=8888, help="listening port", type=int)    
    define("data_dir",              default="", help="cert file path for running with ssl")
    define("cert_file",             default="cert.pem", help="cert file name for running with ssl")
    define("privkey_file",          default="privkey.pem", help="privkey file name for running with ssl")
    define("config_file",           default="",         help="config file path")

###############
# Handlers 
###############
    ''' 
      DeviceHandler:

      Feature:
        Make a bi-directional connection between rhizosphere and device, according to the hand shake request from device.
        Then wait message from rhizospere and return response from device.

    '''
    define("device_route",         default="/device", help="route of request to make a connection with device, and add it to rhizospere.", metavar="/route")
    define("device_module",        default="",        help="[mandatory] module name of rhizome")
    define("device_handler",       default="",        help="[mandatory] handler class name of rhizome")

    ''' 
      WebPortalPageHander:

      Feature:
        Provide portal web interface.
      
    '''
    define("webportalpage_route",         default="/",        help="route of devices",metavar="/route")
    define("webportalpage_module",        default="",         help="[mandatory] module name of rhizome")
    define("webportalpage_handler",       default="",         help="[mandatory] handler class name of rhizome")

    ''' 
      WebCommandPageHandler:

      Feature:
        Provide command sending UI as web.
      
    '''
    define("webcommandpage_route",         default="/command", help="route of devices",metavar="/route")
    define("webcommandpage_module",        default="",         help="[mandatory] module name of rhizome")
    define("webcommandpage_handler",       default="",         help="[mandatory] handler class name of rhizome")

    ''' 
      ClientHandler:

      Feature:
        Make a bi-directional connection between rhizosphere and client, according to the hand shake request from client.
        Then wait message from rhizospere and return response from client.

    '''
    define("client_route",         default="/client/(.*)", help="route of request to make a connection between client and device specified by id, and add it to rhizospere.",metavar="/device/*device_id*")
    define("client_module",        default="",         help="[mandatory] module name of rhizome")
    define("client_handler",       default="",         help="[mandatory] handler class name of rhizome")

###############
# Path 
###############
    define("additional_module_path",default="",         help="path of importing modules",multiple=True, metavar="path1, path2...")
    define("static_path",           default="sample_handlers/static",        help="[mandatory] handler class name of rhizome")
    define("templates_path",        default="sample_handlers/templates",     help="[mandatory] handler class name of rhizome")

    options.parse_command_line()
    if options.config_file:
        options.parse_config_file(options.config_file)
    elif os.path.exists('./config.py'):
        options.parse_config_file('./config.py')

    print(options.additional_module_path)

# https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
    if options.additional_module_path:
        [sys.path.append(x) for x in options.additional_module_path]
#        sys.path.append(options.rhizome_module_path)
    mod_devs = importlib.import_module(options.device_module)
#    mod_devs.cl = cl
    mod_devs.connections = connections
    deviceshandler = getattr(mod_devs, options.device_handler)

    mod_cons = importlib.import_module("sample_consolehandler")
#    mod_cons.cl = cl
    mod_cons.connections = connections
    webportalpagehandler = getattr(mod_cons, "ConsoleHandler")

    mod_cmd = importlib.import_module("sample_commandhandler")
#    mod_cmd.cl = cl
    mod_cmd.connections = connections
    webcommandpagehandler = getattr(mod_cmd, "CommandHandler")

    mod_clt = importlib.import_module("sample_clienthandler")
#    mod_clt.cl = cl
    mod_clt.connections = connections
    clienthandler = getattr(mod_clt, "WebSocketHandler")


# app
    BASE_DIR = os.path.dirname(__file__)
    app = tornado.web.Application([
            (options.device_route,          deviceshandler),
            (options.webportalpage_route,   webportalpagehandler),
            (options.webcommandpage_route,  webcommandpagehandler),
            (options.client_route,          clienthandler),            
#            (r"/console",   consolehandler),
#            (r"/command",   commandhandler),
#            (r"/client/(.*)",    clienthandler),            
        ],
        template_path=os.path.join(BASE_DIR, options.templates_path),
        static_path=os.path.join(BASE_DIR, options.static_path),
    )

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
