# https://stackoverflow.com/questions/64066634/sending-broadcast-in-python

import socket
from time import sleep

def main_function():
    interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]

    print(f"allips: {allips}")

    sent_message_count = 0
    msg = b'hello world'
    while True:
        sent_message_count += 1
        print(f"sent_message_count: {sent_message_count}")

        for ip in allips:
            print(f'sending on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip,0))
            sock.sendto(msg, ("255.255.255.255", 5005))
            sock.close()

        sleep(2)


main_function()
