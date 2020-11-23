# pywsd

Python library for connecting to local instance of [ws-daemon](https://github.com/modulytic/ws-daemon).

## Usage

To connect to a running ws-daemon instance on your machine, create a new WsDaemon object:

```python
from pywsd import WsDaemon

daemon = WsDaemon()
```

This library finds the socket in much the same way as ws-daemon itself does, so you probably do not need to call it with any options. It checks the `WSDAEMON_PREFIX` environment variable, and if that is not set, it defaults to `/root/ws-daemon`. However, you can also pass a path to the constructor which will override these values.

```python
daemon = WsDaemon(prefix="/home/ws-daemon")
```

To execute a script on the remote, use the `execute` method:

```python
status = daemon.execute("test.php", {})
```

This method will return -1 if there is an error with the socket. Otherwise, it will return the exit status of the script.

To execute a command, use either `cmd_local` (for the local machine) or `cmd_remote` (for the remote).

```python
status_local  = daemon.cmd_local("PAUSE", 10000)
status_remote = daemon.cmd_remote("STATUS", {"status": 0, "id": "cf2bf77f-6ad0-47ca-aba7-f300b3c63268"})
```

Finally, to disconnect from the socket, just use the `disconnect` method.

```python
daemon.disconnect()
```

This is also automatically called in the destructor, so you don't need to call it at the end of your script.
