# https://stackoverflow.com/questions/64066634/sending-broadcast-in-python

import contextlib
import socket
import json
from time import sleep

DEFAULT_LOCAL_HOST_UDP_PORT_NUMBER   = 49219

# Ethernet MTU size default 1500
# Maximum packet size is MTU size - IP/UDP packet overhead
DEFAULT_BUFFER_SIZE  = 1400

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

    # Get each network interface's information
    interfaces = socket.getaddrinfo(host=hostname, port=None, family=socket.AF_INET)

    # Break out the IPV4 address of each interface and put them in a new list
    interface_addresses = [ip[-1][0] for ip in interfaces]

    sockets = []

    # gets set in __init__()
    local_host_port_number = None

    def __init__(
            self,
            local_host_port_number=DEFAULT_LOCAL_HOST_UDP_PORT_NUMBER,
            initialize_sockets=True,
    ):
        self.local_host_port_number = local_host_port_number
        if initialize_sockets is True:
            self.initialize_socket_interfaces()

        return

    def __del__(self):
        """
        This gets called when object is destroyed and is used to close all open sockets.
        We suppress exceptions so if things are going badly, they won't be made worse.
        """
        for sock in self.sockets:
            with contextlib.suppress(Exception):
                sock.close()

        return

    def initialize_socket_interfaces(self):
        """
        This routine will create a socket for each interface found in
        self.interface_addresses.  To limit the interface addresses
        to broadcast messages from, remove unwanted addresses from
        the list before calling this method:
            broadcaster = IPV4_UDP_Broadcaster(initialize_sockets=False)
            ... remove unwanted addresses from list ...
            ... then ...
            broadcaster.initialize_socket_interfaces()
        """
        for interface_address in self.interface_addresses:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((interface_address,0))
            self.sockets.append(sock)

        return

    def broadcast(self, message:dict)->int:
        """
        Broadcast UDP packet containing a JSON encoded dictionary (message variable)
        to all devices on each connected LAN (local area network).
        Returns the number of characters/bytes in the sent message.
        """
        json_encoded_message = json.dumps(message)
        udp_message = json_encoded_message.encode('utf-8')

        # sock.sendto() requires something other than a string. E.g. something more binary-ish like
        # a "bytes" class object.
        # The "str" method encode() is used to handle the conversion.
        # Otherwise the following Exception is raised:
        # TypeError: a bytes-like object is required, not 'str'
        for sock in self.sockets:
            sock.sendto(udp_message, ("255.255.255.255", DEFAULT_LOCAL_HOST_UDP_PORT_NUMBER))

        return len(udp_message)

# This runs when we are executing this program using the command line - python all_talk.py
if __name__ == "__main__":
    broadcaster = IPV4_UDP_Broadcaster()

    message = {
        'from_host': broadcaster.hostname,
        'message_count': 0,
        'message': "message text goes here",
    }

    # Run forever
    while True:
        message['message_count'] += 1

        udp_message_length = broadcaster.broadcast(message)

        print(f"message number {message['message_count']} has {udp_message_length} bytes")

        sleep(5)
