from pywsd import WsDaemon

daemon = WsDaemon()
status = daemon.execute("test.php", {})
print(status)
