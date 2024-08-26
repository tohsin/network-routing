import argparse
from client import Client


def main():
    parser = argparse.ArgumentParser(description="Client Messaging Routing Application")
    parser.add_argument("hostname", help="Server hostname")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("socket_type", choices=["TCP", "UDP"], help="Socket type (TCP or UDP)")
    parser.add_argument("mode", choices=["send", "receive"], help="Operation mode")
    parser.add_argument("file", nargs="?", help="File contianing message to send")

    args = parser.parse_args()
    _client = Client(args.hostname, args.port, args.socket_type, args.file)
    _client.run( args.mode)

if __name__ == "__main__":
    main()
#python3 p1client.py 127.0.0.1 5555 UDP send message1.txt
#python3 p1client.py 127.0.0.1 5555 UDP receive message1.txt