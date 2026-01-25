### Run #2 of the python challenge from beginning
# Level 14 - "http://www.pythonchallenge.com/pc/return/italy.html"

from xmlrpc.client import ServerProxy, Transport
import http.client

class NoGzipTransport(Transport):
    def send_headers(self, connection, headers):
        # Remove Accept-Encoding entirely
        headers = [(k, v) for (k, v) in headers if k.lower() != "accept-encoding"]
        super().send_headers(connection, headers)

transport = NoGzipTransport()

server = ServerProxy(
    "http://www.pythonchallenge.com/pc/phonebook.php",
    transport=transport
)

print(server.phone("Bert"))