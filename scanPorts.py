from scapy.all import ARP, Ether, srp
import socket

# Function to scan for devices on the network
def scan_network(ip_range):
    print(f"Scanning IP range: {ip_range}")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    print("Devices found:")
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")
    
    return devices

# Function to check if a specific port is open
def check_open_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # timeout in seconds
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

# Main function
if __name__ == "__main__":
    ip_range = "192.168.1.1/24"  # Change this to your network's IP range
    devices = scan_network(ip_range)

    # List of ports to check
    ports_to_check = {
        22: "SSH",
        21: "FTP",
        5060: "SIP",
        23: "Telnet",
        161: "SNMP"
    }

    # Check for open ports
    for device in devices:
        ip = device['ip']
        print(f"Checking ports on {ip}:")
        for port, service in ports_to_check.items():
            if check_open_port(ip, port):
                print(f"{service} (port {port}) is open on {ip}")
            else:
                print(f"{service} (port {port}) is closed on {ip}")