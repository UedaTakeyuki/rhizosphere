protocol = "wss:"

device_module  = "sample_deviceshandler"
webportalpage_module = "sample_consolehandler"
webcommandpage_module = "sample_commandhandler"
client_module = "sample_clienthandler"

data_dir = "/etc/letsencrypt/live/titurel.uedasoft.com/"
additional_module_path    = ["test", "sample_handlers"] 
#rhizome_module_name  = "a"
device_handler = "WebSocketHandler"
device_route = "/websocket"
