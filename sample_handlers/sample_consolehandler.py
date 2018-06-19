import tornado.web
import pprint

class ConsoleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(pprint.pformat(cl))
        self.write(pprint.pformat(connections))
