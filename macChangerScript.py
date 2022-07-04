#!usr/bin/env python3
import subprocess
import optparse
import re


# function for getting input arguments from the user
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface name for which MAC address is to be changed")
    parser.add_option("-m", "--mac", dest="nmac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.nmac:
        parser.error("[-] Please specify a new mac address, use --help for more info")
    return options


# function for changing the MAC Address
def change_mac(interface, n_mac):
    print("[+] Changing the MAC Address of " + interface + " to " + n_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", n_mac])
    subprocess.call(["ifconfig", interface, "up"])


# function for getting the current MAC Address of the interface
def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig", interface])
    mac_address_search_output = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_output))
    if mac_address_search_output:
        return mac_address_search_output.group(0)
    else:
        print("[-] Mac Address not found & hence cannot be changed!")


options = get_arguments()   # options contain interface and new mac address
current_mac = get_current_mac(options.interface)   # current_mac has the current MAC Address of the interface
# if MAC address exists for the interface then the following code executes
if current_mac:
    print("[+] Current MAC Address: " + str(current_mac))
    change_mac(options.interface, options.nmac)
    current_mac = get_current_mac(options.interface)
    if current_mac == options.nmac:
        print("[+] MAC Address is changed to: " + current_mac)
    else:
        print("[-] MAC Address is not Changed!")


