#-*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket
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
#   app.listen(8888)
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    data_dir = "/etc/letsencrypt/live/titurel.uedasoft.com/"
    ssl_ctx.load_cert_chain(os.path.join(data_dir, "cert.pem"),
                            os.path.join(data_dir, "privkey.pem"))
    http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
