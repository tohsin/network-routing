import argparse
from server import Server


def main():
    parser = argparse.ArgumentParser(description="Client Messaging Routing Application")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("socket_type", choices=["TCP", "UDP"], help="Socket type (TCP or UDP)")
    

    args = parser.parse_args()
    _server = Server( args.port, args.socket_type)
    _server.run()

if __name__ == "__main__":
    main()
