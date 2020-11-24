# __init__.py
# Noah Sandman <noah@modulytic.com>

import os
import json
import socket

from uuid import uuid4


# Code to return if socket breaks
SOCKET_FAILURE = -1


class WsDaemon:
    # TODO add timeout for our socket-getting loops
    def __init__(self, prefix=None):
        self.__prefix = os.getenv("WSDAEMON_PREFIX", "/root/ws-daemon") if prefix is None else prefix

        # socket is kept in prefix folder
        socket_path = self.__get_prefix_file("ws-daemon.sock")
        if os.path.exists(socket_path):
            self.__client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.__client.connect(socket_path)
        else:
            raise Exception("Daemon does not appear to be running: %s does not exist" % (socket_path))


    def __del__(self):
        self.disconnect()


    def disconnect(self):
        self.__client.close()
        

    # execute a script on remote
    def execute(self, script, params):
        # we need a unique ID so we can make sure the response is meant for us
        request_id = str(uuid4())
        sent = self.__send_payload(script, params, request_id=request_id)
        if not sent:
            return SOCKET_FAILURE

        # keep getting responses until we get ours
        while True:
            socket_response = self.__socket_recv()
            if not socket_response:
                return SOCKET_FAILURE

            try:
                res_parsed = json.loads(socket_response)

                # check if valid JSON and if is for us
                valid_response = ("status" in res_parsed) and ("id" in res_parsed)

                if valid_response and (res_parsed["id"] == request_id):
                    return res_parsed["status"]
            except (ValueError, KeyError):          # could not decode json, does not have correct params
                pass


    def cmd_local(self, cmd, data=None):
        return self.__send_cmd_payload("+cmd", cmd, data)


    def cmd_remote(self, cmd, data=None):
        return self.__send_cmd_payload("&cmd", cmd, data)


    # returns true on success, false on failure
    def __send_payload(self, name, params, request_id=None):
        payload = {
            "name": name,
            "params": params
        }

        if request_id:
            payload["id"] = request_id

        payload_bytes = json.dumps(payload).encode("utf-8")

        sent = self.__client.send(payload_bytes)
        return (sent != 0)      # 0 means failure


    def __send_cmd_payload(self, name, cmd, data):
        return self.__send_payload(name, {
            "code": cmd,
            "data": data
        })

    
    # get file from prefix folder
    def __get_prefix_file(self, file, subdir=""):
        new_file = file
        if subdir:
            new_file = os.path.join(subdir, file)

        return os.path.join(self.__prefix, new_file)


    # receive a full message from socket
    def __socket_recv(self):
        chunks = []
        while True:
            chunk = self.__client.recv(2048)
            if chunk == "":         # this is only returned if the socket closes
                return None

            chunks.append(chunk)

            # If we are at the end of JSON, we don't want to receive any more
            # this is a way of getting around the fixed-length thing
            if b"}\n" in chunk:
                break

        return b"".join(chunks)
