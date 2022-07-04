import scapy.all as scapy
import argparse


# function for getting user input as arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="ip_address", help="[-] Specify the IP of the target network")
    (options, arguments) = parser.parse_args()
    if not options.ip_address:
        parser.error("[-] Specify the IP or use --help for more information")
    else:
        return options.ip_address


# function for scanning the network that returns IP addressing & MAC address of the targets
def scan(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast/arp_packet
    answered = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list


# function that prints the IP and MAC of the targets
def print_targets(targets):
    print("IP\t\t\tMac Address\n-------------------------------------------")
    for target in targets:
        print(target["ip"] + "\t\t" + target["mac"])


# main code
ip_address = get_arguments()
targets = scan(ip_address)
print_targets(targets)

