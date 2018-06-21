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
