import socket
import concurrent.futures

def scan_port(target, port, output_file):
    """Scans a single port on a target host and writes the result to a file."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Adjust timeout as needed
            result = s.connect_ex((target, port))
            if result == 0:
                # Port is open
                print(f"Port {port} is open")
                with open(output_file, "a") as f:
                    f.write(f"Port {port} is open\n")
            else:
                # Port is closed or blocked
                print(f"Port {port} is closed or blocked")
                with open(output_file, "a") as f:
                    f.write(f"Port {port} is closed or blocked\n")
    except socket.error:
        # If there is a socket error, the target might be down
        print(f"Could not connect to {target}. The target may be down or unreachable.")
        with open(output_file, "a") as f:
            f.write(f"Could not connect to {target}. The target may be down or unreachable.\n")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")  # Print any scanning errors

def scan_ports(target, start_port, end_port, output_file):
    """Scans a range of ports on a target host and writes results to a file."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port, output_file) for port in range(start_port, end_port + 1)]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    target = input("Enter target IP address: ")
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))
    output_file = input("Enter the name of the output results file (e.g., results.txt): ")  # Prompt for output file name

    print(f"Scanning {target} from port {start_port} to {end_port}...")
    scan_ports(target, start_port, end_port, output_file)

    print(f"Results saved to {output_file}")