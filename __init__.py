# __init__.py
# Noah Sandman <noah@modulytic.com>

import os
import socket

# send data to ws-daemon through Unix socket
def wsdae_send(data):
    socket_path = "/root/ws-daemon/ws-daemon.sock"

    if os.path.exists(socket_path):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(socket_path)
        client.send(data)
        client.close()

        return True
    else:
        return False