from socket import *
import threading
from queue import Queue
# utility functions required to convert string to and from byte data
from utility import byte_encode, byte_decode

"""
Server Class

This class implements a server that can handle both UDP and TCP connections.
It provides functionality to send and receive messages, as well as shut down the server.
"""

class Server:
    """
    Initialize the Server.

    Args:
        socket_type (str): The type of socket, either "UDP" or "TCP".
        port (int): The port number on which the server will operate.
    """

    def __init__(self, socket_type, port) -> None:
        ch_data_size = 4
        max_characters =  3000
        self.buffer_size = max_characters * ch_data_size # buffer size here is 3000 chracters * 4 bytes(size of ch)
        self.port = port
        self.buffer = Queue() # using race condiion safe Queue buffer
        self._socket = None
        self.number_clients = 5
        self.socket_type = socket_type

        # call server setup based on the socket type
        if socket_type == "UDP":
            self.setup_udp_socket()
        else:
            self.setup_tcp_socket()

    '''
    Main function called to start the server
    runs the server loops depending on the socket type chosen by user
    '''
    def run(self):
        
        if self.socket_type == "UDP":
            self.run_udp()

        elif self.socket_type == "TCP":
            self.run_tcp()


    def run_udp(self):
        """
        Run the UDP server loop.
        Continuously receive data and handle it in separate threads.
        """
        while True:
            data, client_address = \
                    self._socket.recvfrom(self.buffer_size) # we wait till we receive data through the socket
            #when we receive receive data from a client we start a sperate thread to process the data and continue the loop
            client_handler =  threading.Thread(target= self.handle_received_data, args=(data, client_address,))
            client_handler.start()  # start the thread
    def run_tcp(self):
        """
        Run the TCP server loop.
        Accept client connections and handle each in a separate thread.
        """
        print("Running TCP Server loop")
        while True:
            # we wai till a client socke attempts to create a handshake with the server
            client_socket, client_address = \
                self._socket.accept()
            print("Client socket found!")
            # After a client is found we start a thread to start processing the data from the client
            client_handler =  threading.Thread(target= self.handle_tcp_client, args=(client_socket, client_address,))
            client_handler.start() # start the thread

    
    def handle_received_data(self, byte_data, client_address, client_socket = None):
        """
        Process received data from clients.

        Args:
            byte_data: The received data in bytes.
            client_address: The address of the client.
            client_socket (socket, optional): The client socket for TCP connections.

        Commands:
            SEND: Cache the received message in Queue.
            RECEIVE: Send the oldest cached message to the client.
            SHUTDOWN: Close the server.
        """
        data =  byte_decode(byte_data) # we convert the byte data to readale string
        command, message = data.split(':', 1) # we expect the client to prepend the task they wish to perfom in the string 

        # if the client just inteded to send a message we simply cache the message into a queue
        if command == "SEND": # message was sent to the server so we cache here 
            self.buffer.put(message)# cache to race condition safe Queue data strcture
            print("Message Received: ", message )
            print("From Address:", client_address)

        # the client intends to receive a messsage sent from some the first client message still in cache
        elif command == "RECEIVE":
            # default reply message incase no message was found in cache
            queued_message = "ERROR: No Message Available at this time Sorry!"

            #if a message is avaible in cache we simply pop from the queue and serve it to the client
            if not self.buffer.empty():
                queued_message = self.buffer.get()

            #depending on the socket type we send the reply back to the client after encoding back to bytes
            if self.socket_type == "UDP":
                #For UDP we need to specify the client address and then send the message
                self._socket.sendto(byte_encode(queued_message), client_address)

            elif self.socket_type == "TCP":
                #in the case of tcp we have an established socket with 
                #the client so we simply send our message through that client socket
                client_socket.send(byte_encode(queued_message))

        elif command == "SHUTDOWN":
            self._socket.close()
            print("Server Closed")
        else:
            # Error handling
            print("Command not found! Accepted Commands are SEND,  RECEIVE, SHUTDOWN")


    def handle_tcp_client(self, client_socket, client_address ):
        """
        Handle TCP client connections.
        Thread function that continuously receive and process data from the client.

        Args:
            client_socket: The connected client socket.
            client_address: The address of the client.
        """
        while True:
            try:
                data = client_socket.recv(self.buffer_size)
                if not data:
                    break # end loop
                #finally we calle the function that prepocess the data and computation the server needs to perform
                self.handle_received_data(data, client_address, client_socket) 
            except Exception as e:
                print("Something Broke trying to communicate with: ", client_address )

    # implements the diffrent protocols UDP and TCP

    def setup_udp_socket(self):
        """
        Set up the UDP socket for the server.
        """
        self._socket = socket(AF_INET, 
                         SOCK_DGRAM) # sock_Dgram selects the udp protocol
        self._socket.bind(('', self.port)) # assings port number to server socket

        print("UDP Server up and running")

    def setup_tcp_socket(self):
        """
        Set up the TCP socket for the server.
        """
        self._socket = socket(AF_INET, SOCK_STREAM) # sock_stream
        self._socket.bind(('', self.port))

        # we also need to establish the number of connections we are expecting the requirement says 3 clients so we pass 3+ as the variable
        self._socket.listen(self.number_clients)
        print("TCP Server up and running")