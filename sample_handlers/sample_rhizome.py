import tornado.websocket
from tornado import gen
import json
import sys
import traceback
from pprint import pprint

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        print ("open")
        pprint(args)
        pprint(kwargs)
        pprint(vars(self.request.headers))
        pprint(vars(self))
        pprint(self.request.headers.get('X-Custome-Aho'))
        pprint(self.request.headers.get('Authorization'))
        pprint(self.request.headers.get('Authorization').startswith('Bearer '))
        
        if self not in cl:
            cl.append(self)

#        super(WebSocketHandler, self).set_status(401)
#        super(WebSocketHandler, self).set_header('WWW-Authenticate','Basic realm="%s"' % "aho")
#        self.close()

    @gen.coroutine
    def on_message(self, message):
        try: 
            ms = json.loads(message)
            if ms["command"] == "register":
                connections[ms["id"]] = {"cn": self}
                print ("register {}".format(ms["id"]))
        except:
            info=sys.exc_info()
            print (traceback.format_exc(info[0]))
            pass

        print ("on_message")
#        while True:
#            yield gen.sleep(3)
#            self.write_message(message + "hello")
 
    def on_close(self):
        print ("close")
        if self in cl:
            cl.remove(self)
        if self in cl:
            cl.remove(self)

