#-*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options
import time
import ssl
import os
 
cl=[]

#クライアントからメッセージを受けるとopen → on_message → on_closeが起動する
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    #websocketオープン
    def open(self):
        print ("open")
        if self not in cl:
            cl.append(self)
 
    #処理
    def on_message(self, message):
        print ("on_message")
#        time.sleep(3600)
        for client in cl:
            print (message)
            #クライアントへメッセージを送信
            client.write_message(message + " webSocket")
 
    #websockeクローズ
    def on_close(self):
        print ("close")
        if self in cl:
            cl.remove(self)

app = tornado.web.Application([
    (r"/websocket", WebSocketHandler)
])

if __name__ == "__main__":
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
