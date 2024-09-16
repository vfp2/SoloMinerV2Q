# Solo Miner V2Q
Solo Miner with High Speed for mining Bitcoin With all System experimenting with a quantum algorithm twist.


![Solo Miner V2](https://raw.githubusercontent.com/vfp2/SoloMinerV2Q/mainx/CaptureScreenSolo.JPG)

Developed using Python 3.11.

First install the required packages :
```
pip install -r requirements.txt
```


These package imports are used:

```
import binascii
import hashlib
import json
import logging
import random
import socket
import threading
import time
import traceback
from datetime import datetime
from signal import SIGINT , signal
import requests
from colorama import Back , Fore , Style
import context as ctx
```

To insert your BTC Wallet Address in `SoloMinerV2.py` change this line:

```

# Changed this Address And Insert Your BTC Wallet

address = '33p9y6EstGYcnoTGNvUJMEGKiAWhAr1uR8' 

``` 

## Credits

Forked from [Solo Miner V2](https://github.com/Pymmdrza/SoloMinerV2) by [@MrPyMmdrza](https://t.me/MrPyMmdrza)