import socket
import os
import struct
from ctypes import *

# length of IP header w/o opt-field
IP_HEADER_LENGTH = 20

# host to listen on
HOST = "192.168.178.32"


def create_ip_payload(data_buffer, num_bytes_opt_data, num_bytes_ip_data):
    """ set the options field of the IP header dynamically depending on the given length
        set the ip-data of the IP frame
    """
    class IP_data(Structure):
        _fields_ = [
            ("opt",     (c_ubyte * num_bytes_opt_data)),
            ("ip_data", (c_ubyte * num_bytes_ip_data))
            ]

        def __new__(cls, data_buffer=None):
            """ create opt fields from given data (starts right after dst-address field) and ip-data
                which starts right after opt-field
            """
            return cls.from_buffer_copy(data_buffer)

        def __init__(self, data_buffer=None):
            """ set length of both fields """
            self.opt_length = num_bytes_opt_data
            self.ip_data_length = num_bytes_ip_data

    return IP_data(data_buffer)


# IP header
class IP(Structure):
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("frame_length_hi", c_ubyte),
        ("frame_length_lo", c_ubyte),
        ("id_hi",           c_ubyte),
        ("id_lo",           c_ubyte),
        ("offset_hi",       c_ubyte),
        ("offset_lo",       c_ubyte),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum_hi",          c_ubyte),
        ("sum_lo",          c_ubyte),
        ("src",             c_ulong),
        ("dst",             c_ulong)
        ]

    def __new__(cls, socket_buffer=None):
        """ create the c_types structure by copying the given buffer and return it"""
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # map protocol constants to their names
        self.protocol_map = {1:"ICMP", 2:"IGMP", 6:"TCP", 17:"UDP"}

        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

        # header length := #32-bit words in header (including options field)
        self.nb_bytes_of_header = (self.ihl * 4)

        # create 16-bit values out of bytes
        self.frame_length = (self.frame_length_hi << 8) + self.frame_length_lo
        self.id = (self.id_hi << 8) + self.id_lo
        self.offset = (self.offset_hi << 8) + self.offset_lo
        self.sum = (self.sum_hi << 8) + self.sum_lo

        # compute #bytes of options-field and data-field
        self.nb_bytes_of_opt_field = self.nb_bytes_of_header - IP_HEADER_LENGTH
        self.nb_bytes_of_data_field = self.frame_length - self.nb_bytes_of_header

        # create IP options field using known IP header length of 20 bytes (w/o opt-field)
        print("[*] Header length in bytes: {}".format(self.nb_bytes_of_header))
        print("[*] Creating options field out of {} bytes".format(self.nb_bytes_of_opt_field))
        print("[*] Creating ip-data out of {} bytes".format(self.nb_bytes_of_data_field))
        ip_data_field = create_ip_payload(socket_buffer[IP_HEADER_LENGTH:], self.nb_bytes_of_opt_field, self.nb_bytes_of_data_field)


# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((HOST, 0))

# IP headers included in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# when using Windows, send an IOCTL to set up promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        # read in packet
        raw_buffer = sniffer.recvfrom(65565)[0]

        print("#####################################################################################")

        # create an IP header (20 bytes := header without options field)
        ip_header = IP(raw_buffer)

        # print out the protocol that was detected and the hosts
        print("[+] Protocol IPv{}: {} {} -> {}".format(ip_header.version,
            ip_header.protocol, ip_header.src_address, ip_header.dst_address))

        # total number of bytes of IP frame
        print("[*] ----- Total length of IP frame: {} bytes".format(ip_header.frame_length))

        # number of 32-bit words in header without options-field would be 5 (160 bits := 20 bytes)
        print("[*] ----- Length of IP header: {} bytes".format(ip_header.nb_bytes_of_header))

# CTRL-C
except KeyboardInterrupt:
    # when using Windows, turn off promiscuous mode
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
