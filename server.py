from socket import *
import threading
from queue import Queue
class Server:

    def __init__(self, socket_type, port) -> None:
        self.buffer_size = 2048
        self.port = port
        self.buffer = Queue() # using thread safe buffer
        self._socket = None

        if socket_type == "UDP":
            self.setup_udp_socket()

    def run(self):
        # here we handle receiving msgs in infinte loop
        while True:
            data, client_address = \
                    self._socket.recvfrom(self.buffer_size)
            
            # if client_address is not None:
            client_handler =  threading.Thread(target= self.handle_received_data, args=(data, client_address,))
            client_handler.start()
           
    def handle_received_data(self, byte_data, client_address):
        data = byte_data.decode('utf-8')
        command, message = data.split(':', 1)

        if command == "SEND": # message was sent to the server so we cache here 
            self.buffer.put(message)
            print("Message Received: ", message )
            print("From Address:", client_address)

        elif command == "RECEIVE":
            queued_message = "ERROR: No Message Available at this time Sorry!"
            if not self.buffer.empty():
                queued_message = self.buffer.get()
            self._socket.sendto(queued_message.encode('utf-8'), client_address)
                
        elif command == "SHUTDOWN":
            self._socket.close()
            print("Server Closed")
        else:
            # Error handling
            print("Command not found! Accepted Commands are SEND,  RECEIVE, SHUTDOWN")


    # implements the diffrent protocols UDP and TCP
    def setup_udp_socket(self):
        self._socket = socket(AF_INET, 
                         SOCK_DGRAM) # sock_Dgram selects the udp protocol
        self._socket.bind(('', self.port)) # assings port number to server socket

        print("Server up and running")


server = Server("UDP", 5555)
server.run()