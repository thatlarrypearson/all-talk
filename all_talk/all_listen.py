# all-talk/all_talk/all_listen.py
import socket
import json

DEFAULT_LOCAL_HOST_INTERFACE_ADDRESS = "0.0.0.0"
DEFAULT_LOCAL_HOST_UDP_PORT_NUMBER   = 49219

# Ethernet MTU size default 1500
# Maximum packet size is MTU size - IP/UDP packet overhead
DEFAULT_BUFFER_SIZE  = 1400

class IPV4_UDP_Receiver(object):
    """
    Listen on UDP port for JSON data.

    Parse JSON encoded records and return dictionary
    """
    message_count = 0
    logger = None
    message_receiver = None

    def __init__(
        self,
        local_host_interface_address=DEFAULT_LOCAL_HOST_INTERFACE_ADDRESS,
        local_host_udp_port_number=DEFAULT_LOCAL_HOST_UDP_PORT_NUMBER,
    ):
        self.local_host_interface_address = local_host_interface_address
        self.local_host_udp_port_number = local_host_udp_port_number

        # Create an IPV4 socket to handle UDP messages
        self.message_receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind or associate this socket to every IPV4 interface (except possibly loopback 127.0.0.1)
        # on this host for the given UDP port number
        self.message_receiver.bind((local_host_interface_address, local_host_udp_port_number))

    def __iter__(self):
        """Start iterator."""
        return self

    def __next__(self):
        """
        Get the next iterable.   Returns raw data dictionary.
        """
        # message is type bytes, JSON encoded
        # sending_ip_endpoint is list [Sender IP Address:str, Sender Port Number int]
        message, sending_ip_endpoint = self.message_receiver.recvfrom(DEFAULT_BUFFER_SIZE)
        self.message_count += 1

        try:
            # if weird decode errors, then use 'ignore' in: message.decode('utf-8', 'ignore')
            # message_dict = json.loads(message.decode('utf-8'))
            message_dict = json.loads(message)

        except json.decoder.JSONDecodeError as e:
            # improperly closed JSON record
            print(f"{self.message_count}: Corrupted JSON info in message {message}\n{e}")
            return None

        if not isinstance(message_dict, dict):
            print(f"{self.message_count}: JSON decode didn't return a dict: {message}")
            return None

        # add the sending IP endpoint to the message dictionary
        message_dict['sending_ip_endpoint'] = {
            'ip_address': sending_ip_endpoint[0],
            'port_number': sending_ip_endpoint[1],
        }
        return message_dict

# This runs when we are executing this program using the command line - python all_talk.py
if __name__ == "__main__":

    udp_received_messages = IPV4_UDP_Receiver()

    for message in udp_received_messages:
        print(f"Message Number {udp_received_messages.message_count}, Message: {message}")
