from socket import *
from utility  import byte_decode, byte_encode

"""
A client class that abstracts and performs operations required to communicate with a server.
Supports both UDP and TCP protocols.
"""
class Client:
    """
    Initialize the Client with connection details and message file location.

    Args:
        hostname (str): Server hostname or IP address.
        port (int): Server port number.
        socket_type (str): Socket type, either "UDP" or "TCP".
        file_dir (Optional[str]): Directory of the message file for sending.
    """
    def __init__(self,hostname, port, socket_type, file_dir = None) -> None:
        ch_data_size = 4
        max_characters =  3008
        self.buffer_size = max_characters * ch_data_size
        self.file_dir = file_dir
        self._socket = None
        self.hostname = hostname
        self.port = port
        self.socket_type = socket_type

        # we call the initlaiser depeding on the Socket type selected by the user
        if socket_type == "UDP":
            self.setup_udp_protocol()
        elif socket_type == "TCP":
            self.setup_tcp_protocol()

    # The main fucntion that runs the client and depends on the mode (Send, receive) the user wishes to perform
    def run(self, mode ):
        """
        Run the client in either send or receive mode.

        Args:
            mode (str): Either "send" or "receive".

        Raises:
            ValueError: If an invalid mode is provided.
        """
        processed_data = self.prepend_command(mode)
        if mode == "send":
            self.send_message(processed_data)
        elif mode== "receive":
            self.request_reply(processed_data)
        else:
            raise ValueError("Invalid mode. Must be either 'send' or 'receive'.")

    def prepend_command(self, mode):
        """
        Prepend the corresponding command to the message based on the mode.

        Args:
            mode (str): Either "send" or "receive".

        Returns:
            str: Processed data with prepended command.
        """
        data = " "
        if mode == "send":
            # we Prepend the SEND string to the message we wish to send
            data = self.process_txt() # read the message from the file passed from the user
            self.cache_msg = data
            data = "SEND:" + data # prepend SEND  to message string

        # we dont really send anything when we want to receive data so we prepend "RECEIVE:" to an empty string
        elif mode == "receive":
            data = "RECEIVE:" + data
        else:
            data = ""
        return data

    
    def send_message(self, message):
        """
        Encode and send a message to the server.

        Args:
            message (str): The message to be sent.
        """
        encoded_message = byte_encode(message)

        # method for sending message depends on the socket type chose by user
        if self.socket_type == "UDP":
            self.udp_send_msg(encoded_message)

        elif self.socket_type == "TCP":
            self.tcp_send_msg(encoded_message)

 
    def udp_send_msg(self, byte_msg):
        """Send a UDP message to the server."""
        self._socket.sendto(byte_msg, (self.hostname, self.port)) # to send message we pass hostnamem, port and the message


    def udp_receive_msg(self):
        """Receive a UDP message from the server."""
        received_message, server_address = \
            self._socket.recvfrom(self.buffer_size) # the server send a message through our address
        
        return received_message
    
    def tcp_send_msg(self, byte_msg):
        """Send a TCP message to the server after socket connection has been prviusly established"""
        self._socket.send(byte_msg)


    def tcp_receive_msg(self):
        """Receive a TCP message from the server after the connection ahs been established with the server"""
        received_message = self._socket.recv(self.buffer_size)
        return received_message


    def request_reply(self, request_command):
        """
        Request a reply from the server and print the received message.

        Args:
            request_command (str): The command to send to the server.
        """
        # To request a reply fromt he server we send a message asking for a reply
        self.send_message(request_command)
        received_message = self.udp_receive_msg() if self.socket_type == "UDP" else self.tcp_receive_msg()


        # we decode the message from the server from byte to string
        decoded_message = byte_decode(received_message)
        
        print("Message received:\n"+ decoded_message)            
        self._socket.close() # finally we close the server

   
    def setup_udp_protocol(self):
        """Set up a UDP socket."""

        # In UDP we simply need to create our UDP socket object with sock_Dgram as Socket kind
        self._socket = socket(AF_INET, SOCK_DGRAM) 

    def setup_tcp_protocol(self):
        """Set up a TCP socket and connect to the server."""
        try:
            self._socket = socket(AF_INET, SOCK_STREAM) # In TCP we first create a server with SOCK_STREAM
            self._socket.connect((self.hostname, self.port)) # after server creation we try to connect to the server and perform handshake
            self._socket.settimeout(10)  # Set a 10-second timeout
            print(f"Successfully connected to {self.hostname}:{self.port}")
        except Exception as e:
            self._socket.close()
            raise ConnectionError(f"Failed to connect to {self.hostname}:{self.port}. Error: {e}")
    
    def process_txt(self):
        """
        Read and return the content of the message file.

        Returns:
            str: Content of the message file.

        Raises:
            FileNotFoundError: If the specified file is not found.
            IOError: If there's an error reading the file.
        """
        try:
            with open(self.file_dir , 'r') as file:
                # Read the content of the file
                return file.read()
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_dir}")
            raise
        except IOError as e:
            print(f"Error reading file: {e}")
            raise



