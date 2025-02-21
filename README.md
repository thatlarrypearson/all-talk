# all-talk

IPV4 UDP Packet Broadcast and Receive Classes

## Python Runtime Environment Requirements

Python 3.11 or newer.

## Testing the Classes

Both the ```all_talk.py``` (```IPV4_UDP_Broadcaster``` class) and ```all_listen.py``` (```IPV4_UDP_Receiver``` class) files include a main function that instantiates objects and then runs them in a simple test.

Just run broadcaster and receiver on one or more computers on the same network segment and see what happens.

### How to Run Broadcaster Portion of Test

 ```bash
 python3.11 all_talk.py
 ```

### How to Run Receiver Portion of Test

```bash
python3.11 all_listen.py
```

## Using ```IPV4_UDP_Receiver()``` Class

```bash
from all_talk.all_listen import IPV4_UDP_Receiver

udp_received_messages = IPV4_UDP_Receiver()

for message in udp_received_messages:
    print(f"Message Number {udp_received_messages.message_count}, Message: {message}")
```

## Using ```IPV4_UDP_Broadcaster()``` Class

```bash
from all_talk.all_talk import IPV4_UDP_Broadcaster

broadcaster = IPV4_UDP_Broadcaster()

# create the message to send encoded as a Python dictionary
message = {
    'from_host': broadcaster.hostname,
    'message_count': 1,
    'message': "message text goes here",
}

# Send a single message

udp_message_length = broadcaster.broadcast(message)

print(f"message had {udp_message_length} bytes")
```

## Building and Installing ```all-talk``` Python Package

Installation instructions were written for Raspberry Pi OS 64 bit.

### Is Your Raspberry Pi OS Current?

Run the command ```cat /etc/os-release``` and ```cat /etc/debian_version``` as shown below.

```bash
$ cat /etc/os-release 
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
$ cat /etc/debian_version
12.9
$ 
```

If the debian version is less than *12.9*, then you need to update/upgrade your Raspberry Pi OS.

### Upgrading Your Raspberry Pi OS

Follow these commands to upgrade/update your Raspberry Pi OS:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
```

### Installing a Non-System Version of Python on Raspberry Pi OS

Follow the instructions [here](https://github.com/thatlarrypearson/telemetry-obd/blob/master/docs/Python311-Install.md) for installing Python 3.11.

### Installing This Python Software Package

With some, little or no modification, the installation instructions should work for other Linux based systems.  The amount of effort will vary by Linux distribution with Debian based distributions the easiest.

```bash
git clone https://github.com/thatlarrypearson/all-talk.git
cd all-talk
python3.11 -m build .
python3.11 -m pip install dist/all_talk-0.0.0-py3-none-any.whl
```

## License

[MIT](./LICENSE.md)
