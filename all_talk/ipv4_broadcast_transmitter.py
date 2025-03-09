# ipv4_broadcast_transmitter.py
"""
Class (IPV4_UDP_Broadcaster) with method (broadcast()) that will
broadcast IPV4 UDP JSON messages composed from the contents of the supplied dictionary.

Includes function (get_host_ipv4_interface_addresses()) that will identify available IPV4
network interfaces on the host computer.

See (if __name__ == "__main__":) below for example / simple test.
"""

import contextlib
import socket
import json
from platform import system
from time import sleep

host_os = system()

# Linux or Mac
if host_os == "Linux":
    try:
        import netifaces
    except ModuleNotFoundError as e:
        print("Use 'pip' to install 'netifaces' then try again. ")
        exit(1)

DEFAULT_LOCAL_HOST_INTERFACE_ADDRESS = "0.0.0.0"
DEFAULT_LOCAL_HOST_UDP_PORT_NUMBER   = 49219

# Ethernet MTU size default 1500
# Maximum packet size is MTU size - IP/UDP packet overhead
DEFAULT_BUFFER_SIZE  = 1400

def get_host_ipv4_interface_addresses()->list:
    """
    Get a list of the local host's IPV4 interface addresses
    """
    if host_os == "Windows":
        # Windows
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        return [ip[-1][0] for ip in interfaces]

    # Linux and Mac
    interfaces = netifaces.interfaces()
    return [netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                            for interface in interfaces]

class IPV4_UDP_Broadcaster(object):
    """
    Broadcasts dictionary data type messages to everyone on the local area network
    using IPV4 UDP datagrams/packets.

    Note UDP is not a reliable transport mechanism and limits the size of packets to
    the local area network's MTU (maximum transfer unit) size minus the IP and UDP overhead.

    On Mac/Linux, use command line command "ifconfig" to get each connected network's MTU size.

    On Windows, use command line command "netsh interface ipv4 show subinterfaces" to get each
    connected networks's MTU size.
    """

    # Same as Windows/Mac/Linux command line command "hostname"
    hostname = socket.gethostname()

    socket = None

    def __init__(
            self,
            interface_address:str = DEFAULT_LOCAL_HOST_INTERFACE_ADDRESS,
            port_number:int = DEFAULT_LOCAL_HOST_UDP_PORT_NUMBER,
    ):
        self.port_number = port_number
        self.interface_address = interface_address
        self.initialize_socket_interface(interface_address)

        return

    def __del__(self):
        """
        This gets called when object is destroyed and is used to close all open sockets.
        We suppress exceptions so if things are going badly, they won't be made worse.
        """
        with contextlib.suppress(Exception):
            self.socket.close()

        return

    def initialize_socket_interface(self):
        """
        Create a socket for I/O on self.interface_address 
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind((self.interface_address,0))

        return

    def broadcast(self, message:dict)->int:
        """
        Broadcast UDP packet containing a JSON encoded dictionary (message variable)
        to all devices on each connected LAN (local area network).
        Returns the number of characters/bytes in the sent message.
        """
        json_encoded_message = json.dumps(message)

        # sock.sendto() requires something other than a string. E.g. something more binary-ish like
        # a "bytes" class object.
        # The "str" method encode() is used to handle the conversion.
        # Otherwise the following Exception is raised:
        # TypeError: a bytes-like object is required, not 'str'
        udp_message = json_encoded_message.encode('utf-8')

        self.socket.sendto(udp_message, ("255.255.255.255", self.port_number))

        return len(udp_message)

# This runs when we are executing this program using the command line - python ipv4_broadcast_transmitter.py
if __name__ == "__main__":
    print(f"IPV4 Interface Addresses: {get_host_ipv4_interface_addresses()}")

    broadcaster = IPV4_UDP_Broadcaster()

    message = {
        'from_host': broadcaster.hostname,
        'from_address': broadcaster.interface_address,
        'message_count': 0,
        'message': "message text goes here",
    }

    # Run forever
    while True:
        message['message_count'] += 1

        udp_message_length = broadcaster.broadcast(message)

        print(f"Sent Message Number {message['message_count']} from ",
              f"{broadcaster.hostname}/{broadcaster.interface_address} ",
              f"has {udp_message_length} bytes")

        sleep(5)
