import tornado.websocket
from pprint import pprint

route = "/a/b/c"

class RhizoSphereHandler(tornado.websocket.WebSocketHandler):
    route = "/a/b/c"

    def auth_confirm(self, id, token):
        print ("id = {}".format(id))
        print ("token = {}".format(token))
        return True

    def open(self, id):
#        print ("open")
#        id = self.request.headers.get('Sec-Websocket-Protocol')
        print ("open",id)
        self.id = id
        print (id)
        if id in connections:
            connections[id]["client_socket"] = self    

    def on_message(self, message):
        print ("on_message")
        print(message)
        if self.id in connections:
            if "device_socket" in connections[self.id]:
                connections[self.id]["device_socket"].write_message(message)  
 
    def on_close(self):
        print ("close")
