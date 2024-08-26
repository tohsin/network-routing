from socket import *

class Client:
    def __init__(self,hostname, port, socket_type, file_dir = None) -> None:
        self.buffer_size = 2048
        self.file_dir = file_dir
        self._socket = None
        self.hostname = hostname
        self.port = port

        if socket_type == "UDP":
            self.setup_udp_protocol()

    def run(self, mode ):
        processed_data = self.prepend_command(mode)

        if mode == "send":
            self.send_message(processed_data)
        else:
            self.request_reply(processed_data)

            
    def prepend_command(self, mode):
        data = " "
        if mode == "send":
            # we Prepend the SEND string to the message we wish to send
            data = self.process_txt()
            data = "SEND:" + data

        elif mode == "receive":
            data = "RECEIVE:" + data

        else:
            data = ""
        return data

    def send_message(self, message):
        encoded_message = message.encode('utf-8')
        self._socket.sendto(encoded_message, (self.hostname, self.port))
    
    def request_reply(self, request_command):
        # we actually send message first telling the server to send us some info
        self.send_message(request_command)

        received_message, server_address = \
            self._socket.recvfrom(self.buffer_size)
        
        decoded_message = received_message.decode('utf-8')
        
        print("Message received:\n"+ decoded_message)            
        self._socket.close()


    # implements the diffrent protocols UDP and TCP
    def setup_udp_protocol(self):
        self._socket = socket(AF_INET, SOCK_DGRAM) # sock_Dgram selects the udp protocol


    def tcp_protocol(self):
        pass

    # Function to read the message txt file
    def process_txt(self):
        file_content = None
        try:
            with open(self.file_dir , 'r') as file:
                # Read the content of the file
                file_content = file.read()
        except:
            print("file reading went wrong")
            return
        return file_content



