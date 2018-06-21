import tornado.web
import json

class CommandHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            id      = self.get_argument('id')
            cmd_str = self.get_argument('cmd_str')
            connections[id]["device_socket"].write_message(
                json.dumps({
                    "order": "exec_bash",
                    "cmd_str": cmd_str
                })
            )
        except tornado.web.MissingArgumentError:
            pass

        self.render('client.html', connections=connections)

