import socketserver
import threading
from threading import Thread

addrs = {}
requests = {}
threads = {}


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        name = str(self.request.recv(1024), 'utf8')
        requests[self.request] = name
        cur_thread = threading.current_thread()
        threads[cur_thread] = name
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        self.request.sendall(bytes(welcome, 'ascii'))
        note = "%s has joined the chat!" % name
        broadcast(bytes(note, "utf8"))

        while True:
            pass
            data = self.request.recv(BUFSIZ)
            if data != bytes("{quit}", "utf8"):
                broadcast(data, name + ": ")
                # self.request is the TCP socket connected to the client
                print("{} wrote: {}".format(self.client_address[0], data))
            else:
                self.request.sendall(bytes("{quit}", "utf8"))
                del requests[self.request]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for request in requests:
        request.sendall(bytes(prefix, "ascii") + msg)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 57695
    BUFSIZ = 1024

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    # server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    print("IP: {} Port: {}".format(str(ip), str(port)))
    print("Waiting for connection...")
