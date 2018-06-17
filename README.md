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
<img src="https://github.com/UedaTakeyuki/rhizosphere/blob/master/docs/sequence.png">

## Data
```json
# command
{ 
  "type"  : "comman",
  "id"    :
  "order" : "exec_bash | exec_bash_ret_okng_only | exec_bash_no_return"
}

# response
{ 
  "type"  : "response",
  "id"    : # same id of command
  "resutl" : # string | "ok" or "ng" | null
}
```
