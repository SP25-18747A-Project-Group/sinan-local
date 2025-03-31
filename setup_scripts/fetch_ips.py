import subprocess

# File containing list of SSH commands
NODES_FILE = "nodes.txt"
OUTPUT_FILE = "node_ips.txt"

def get_ip_from_node(ssh_command):
    """Extract hostname from SSH command and fetch its IP address."""
    parts = ssh_command.strip().split()
    if len(parts) != 2 or parts[0] != "ssh":
        print(f"Skipping invalid entry: {ssh_command}")
        return None

    hostname = parts[1]  # Extract user@hostname
    print(f"Fetching IP for {hostname}...")

    try:
        # Run SSH command to fetch the node's IP
        result = subprocess.run(
            ["ssh", hostname, "hostname -I | awk '{print $1}'"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            ip = result.stdout.strip()
            print(f"{hostname} -> {ip}")
            return ip
        else:
            print(f"Error fetching IP for {hostname}: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print(f"Timeout: Unable to reach {hostname}")
        return None

def main():
    try:
        with open(NODES_FILE, "r") as file:
            ssh_commands = file.readlines()
    except FileNotFoundError:
        print(f"Error: {NODES_FILE} not found!")
        return

    node_ips = []

    for ssh_cmd in ssh_commands:
        ip = get_ip_from_node(ssh_cmd)
        if ip:
            node_ips.append(ip)

    # Save IPs to file
    with open(OUTPUT_FILE, "w") as file:
        file.write("\n".join(node_ips))

    print(f"IP addresses saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
