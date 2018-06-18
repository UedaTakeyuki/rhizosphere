import tornado.websocket
from tornado import gen
import json
import sys
import traceback

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print ("open")
        if self not in cl:
            cl.append(self)

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


