import subprocess

def read_nodes(file_path):
    with open(file_path, 'r') as file:
        nodes = [line.strip().split(" ") for line in file.readlines() if line.strip()]
    return nodes

def scp_and_run_script(node_ssh_command, script_path):
    try:
        # Extract the username and host from the SSH command
        username_host = node_ssh_command[1]

        # SCP the script to the node
        print(f"SCP'ing the script to {username_host}...")
        scp_command = f"scp {script_path} {username_host}:/users/{username_host.split('@')[0]}/"
        subprocess.run(scp_command, shell=True, check=True)
        
        # SSH to the node and run the script
        print(f"Running the script on {username_host}...")
        ssh_command = f"ssh {username_host} 'bash /users/{username_host.split('@')[0]}/install_packages.sh'"
        subprocess.run(ssh_command, shell=True, check=True)
        
        print(f"Script successfully executed on {username_host}.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while processing {node_ssh_command}: {e}\n")

def main():
    nodes_file = 'nodes.txt'  # Text file containing SSH commands (e.g., ssh user@node)
    script_path = '/home/shyacinthe/sinan/install_packages.sh'  # Path to your install_packages.sh script
    
    # Read the SSH commands from the file
    nodes = read_nodes(nodes_file)
    print(nodes)
    # SCP the script to each node and run it
    for node_ssh_command in nodes:
        scp_and_run_script(node_ssh_command, script_path)

if __name__ == "__main__":
    main()
