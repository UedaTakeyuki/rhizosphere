# rhizosphere
root server for collaborative devices

## Vision
* Provide bi-directional continuous connection for tens of thousands of devices over NAT.
* Provide console feature of these devices.
* Provide ***Server side device programming*** foundations.

## Architecture
* ***rhizospere :*** Centoral server which provide these features mentioned above.
* ***[hypha](https://github.com/UedaTakeyuki/hypha) :*** Device controller. 

<div class="mermaid">
    sequenceDiagram
      A ->> B  : 要求
      B -->> A : 返答
</div>
<script src="https://unpkg.com/mermaid/dist/mermaid.min.js"></script>
