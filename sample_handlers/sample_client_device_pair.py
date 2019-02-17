#-*- coding:utf-8 -*-
# Copy Right Takeyuki UEDA  © 2018 -

import tornado.websocket
import tornado.web
from tornado import gen

from tornado.log import app_log

'''
A global variable of dictionaly "connections" should be added at outside of this module,
 and share between rhizosphere main function.
'''

type = "RS_cdpair_and_connections_shares"
connections_shares = ["RS_WebPortalPageHander", "RS_WebCommandPageHandler"]


class RS_ClientHandler(tornado.websocket.WebSocketHandler):
    route = "/client/(.*)"

    def auth_confirm(self, id, token):
        app_log.info("auth_confirm:")
        app_log.info("id =  %s", id)
        app_log.info("token = %s", token)
        return True

    def open(self, id):
        app_log.info("open: id =  %s", id)
        self.id = id
        if id in connections:
            connections[id]["client_socket"] = self    

    def on_message(self, message):
        app_log.info("on_message: message =  %s", message)
        if self.id in connections:
            if "device_socket" in connections[self.id]:
                connections[self.id]["device_socket"].write_message(message)  
 
    def on_close(self):
        app_log.info("close:")

    # accept all cross-origin traffic 
    # http://www.tornadoweb.org/en/stable/websocket.html#tornado.websocket.WebSocketHandler.check_origin
    def check_origin(self, origin):
        return True



class RS_DeviceHandler(tornado.websocket.WebSocketHandler):
    route = "/device"

    def auth_confirm(self, id, token):
        app_log.info("auth_confirm:")
        app_log.info("id =  %s", id)
        app_log.info("token = %s", token)
        return True

    def open(self):
        app_log.info("open:")
        app_log.info("request headers = %s", ','.join(self.request.headers.keys()))
        id = self.request.headers.get('X-Custome-Id')
        if self.request.headers.get('Authorization').startswith('Bearer '):
            token = self.request.headers.get('Authorization')[6:]
        
        # confirm authentication
        if self.auth_confirm(id, token):
            # register
            self.id = id
            connections[id] = {"device_socket": self}
            app_log.info("register id =  %s", id)
        else:
            # close
            self.close()
            return False

    @gen.coroutine
    def on_message(self, message):
        app_log.info("on_message: message =  %s", message)
        if "client_socket" in connections[self.id]:
            connections[self.id]["client_socket"].write_message(message)
 
    def on_close(self):
        app_log.info("close:")
        if self.id:
            if self.id in connections:
                connections.pop(self.id)


class RS_WebPortalPageHander(tornado.web.RequestHandler):
    route = "/"
    def get(self):
        self.render('index.html', connections=connections)

class RS_WebCommandPageHandler(tornado.web.RequestHandler):
    route = "/command"
    def get(self):
        try:
            id      = self.get_argument('id')
            cmd_str = self.get_argument('cmd_str')
        except tornado.web.MissingArgumentError:
            pass

        self.render('client.html', connections=connections, id=id)
