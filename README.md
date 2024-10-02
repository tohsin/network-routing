# Network Message routing
 
# Setup  and Running Guide

## Create Virtual environment (Optional)

Though not required for this project as the libraries are custom to python

```bash
python3 -m venv venv
source venv/bin/activate
```

## To run Server 
We pass 
1. Port
2. Socket Type

```bash
python3 p1server.py <port> <socket_type>
```

### Example Run TCP Server
```bash
python3 p1server.py 5555 TCP
```


## To run Clients

We pass 
1. Host Name
2. Port
3. Socket Type
4. Mode ["send", "receive"]
5. File location for message in txt

```bash
python3 p1client.py <host_name> <port> <socket_type> <mode> <message_file_path>
```


### Example Send Message to server

Note: We assume the server and the client are on the same machine so we pass "127.0.0.1" as local host in this bash command

```bash
python3 p1client.py 127.0.0.1 5555 TCP send message1.txt
```

# Design Description

## Client 
We take an OOP approach with initialization of client messaging parameters done in the class initializers, taking the hostname, ports, and the socket type.
Depending on the socket type selected by the user, we initialize the socket type in the initializer. This basically initializes the socket object we would be using for handling our operations.
We then have a main function called run where we pass the mode of operation we wish to achieve, i.e., to send or receive a message.
In either case, we prepend the string **SEND:** or **RECEIVE:** to let the server know what to do with the data coming from the client.


### UDP operations

We have two UDP-specific functions that abstract the logic of UDP operations to send and receive messages to a server:

1. UDP Send Message
2. UDP Receive Message


### TCP operations
Similar to UDP, we have TCP-specific methods to send and receive messages. Unlike UDP, when we are setting up, we specify the hostname and port.



## Assumptions
Accounting for 3000 characters, we set the buffer size of the message to approximately 12000 = 3000 * 4.


## Server

This is slightly more complicated than the client code.
We also take an Object-Oriented Programming approach to setting up and running our server. We initialize our server class with the main parameters the users provide: the port and server type.

We then have a main method called run.

### Data structure and Cache

To allow caching of the messages sent from the client on a FIFO basis, we use a Queue. However, we use a Queue provided by the queue library that comes with Python, as we need a queue data structure capable of handling race conditions that might occur when multiple users try to send a message to the server at the same time.


### Handling Concurrency

#### TCP

##### Server Setup
Due to the nature of TCP, we need to set up the number of users we wish to concurrently communicate with the server at the setup, and this is done by:

>self._socket.listen(self.number_clients)

Note that the code to set up the TCP socket is abstracted and is called at the initialization of the Server Class.

###### Handling multiple Clients
The main run function runs an infinite loop waiting for a connection to be established. Upon establishing/accepting a connection, a thread is then created to handle all the operations of the client.

In the thread function, we have another loop that listens for data coming from the client and hands off the data to be processed.

#### UDP

Similar to TCP, we run the function in a main loop that keeps checking for data received in the server's buffer. When data is received, it hands off the data to a thread. In the case of UDP, the thread mostly handles storing data in the queue or retrieving data from the queue.

## Differentiating Client operations

To differentiate the operation the user wishes to perform (either to send or receive a message), we expect that the user prepends their intended use 'SEND:' or "RECEIVE:" to the message they send. We simply process this by splitting the string.

## Assumptions
Similar to the assumption made in client code we assume we are explecting 3000 chracters 