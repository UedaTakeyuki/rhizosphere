import tornado.websocket
import tornado.web
from tornado import gen
from pprint import pprint

'''
A global variable of dictionaly "connections" should be added at outside of this module,
 and share between rhizosphere main function.
'''

type = "RS_cdpair_and_connections_shares"
connections_shares = ["RS_WebPortalPageHander", "RS_WebCommandPageHandler"]


class RS_ClientHandler(tornado.websocket.WebSocketHandler):
    route = "/client/(.*)"

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


class RS_DeviceHandler(tornado.websocket.WebSocketHandler):
    route = "/device"

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


