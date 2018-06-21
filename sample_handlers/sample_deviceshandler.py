import tornado.websocket
from tornado import gen
import json
import sys
import traceback
from pprint import pprint

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def auth_confirm(self, id, token):
        print ("id = {}".format(id))
        print ("token = {}".format(token))
        return True

    def open(self):
        print ("open")
        id = self.request.headers.get('X-Custome-Id')
        token = self.request.headers.get('Authorization').startswith('Bearer ')
        
        # confirm authentication
        if self.auth_confirm(id, token):
            # register
            self.id = id
            connections[id] = {"device_socket": self}
            print ("register {}".format(id))
        else:
            # close
            self.close()
            return False

    @gen.coroutine
    def on_message(self, message):
        print ("on_message")
        print(message)
        if "client_socket" in connections[self.id]:
            connections[self.id]["client_socket"].write_message(message)
 
    def on_close(self):
        print ("close")
        if self.id:
            if self.id in connections:
                connections.pop(self.id)


