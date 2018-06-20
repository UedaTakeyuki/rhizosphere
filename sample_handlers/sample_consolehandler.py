import tornado.web
import pprint

class ConsoleHandler(tornado.web.RequestHandler):
	def get(self):
#   self.write(pprint.pformat(connections))
		self.render('index.html', connections=connections)