# rhizosphere
root server for collaborative devices

## Vision
* Provide bi-directional continuous connection for tens of thousands of devices over NAT.
* Provide console feature of these devices.
* Provide ***Server side device programming*** foundations.

## Architecture
* ***rhizospere :*** Centoral server which provide these features mentioned above.
* ***[hypha](https://github.com/UedaTakeyuki/hypha) :*** Device controller. 

## Sequence
<img src="https://github.com/UedaTakeyuki/rhizosphere/blob/master/docs/sequence2.png">

## Demo
* A ***Raspberry Pi***, running [hypha](https://github.com/UedaTakeyuki/hypha), is connected with ***rhizospere*** by ***3G dongle***.
* Browser connect ***rhizospere***, select ***Device id***.
* Send Bash commands from Browser. Then, the command is ***transit*** to RPi device, ran and return result. 

<video>
  <source src='https://github.com/UedaTakeyuki/rhizosphere/blob/master/docs/rhizosphere.mov' type='video/mp4'>
</video>

<img src="https://github.com/UedaTakeyuki/rhizosphere/blob/master/docs/rhizospere.gif">

[demo movie](https://youtu.be/L_7clcDccdQ) on the youtube.

## Data
```json
# command
{ 
  "type"  : "command",
  "id"    : "id of command",
  "order" : "exec_bash | exec_bash_ret_okng_only | exec_bash_no_return"
}

# response
{ 
  "type"  : "response",
  "id"    : "the same id of command",
  "resutl" : "result string | ok or ng | null"
}
```

## connections

```connections``` is a key parts for interconnection between device and console. connections is a dictionaly which there key is specified by device id. The value of the connection is also dictionalys which has 2 value, one is the device side bi-directional socket and the other is client side bi-directional soket.

```json
connections 
= {
    "device_id": {
       "device_socket": "socket for device", 
       "client_socket": "socket for client"
     }
   }
   
```

### RhizoSpereHandler

```RhizoSpereHandler``` is python key module for handling connection between device and clinet.
RhizoSpereHandler module is set by option or config file specified as rhizosperehandlers, and import dinamically by main.py.
RhizoSpereHandler module must have a string member variable, named "type", which specifies a manner of initialization.

Following type string are available.

#### RS_cdpair_and_connections_shares

This type of RhizoSpereHandler is for a connections and several classes which share the connections as module global.
These classes are as follows:
- class for device handler, named RS_DeviceHandler
- class for client handler, named RS_ClientHandler
- other classes use the connections, for example, provide Web UI, IoT connection and so on.

Other classes mentioned above should be listed up by the module member of connections_shares like:
```
connections_shares = ["RS_WebPortalPageHander", "RS_WebCommandPageHandler"]
```
