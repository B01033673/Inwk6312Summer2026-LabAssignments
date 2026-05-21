import logging
from netmiko import ConnectHandler
import yaml

# Suppress Netmiko debug messages
logging.getLogger("paramiko").setLevel(logging.WARNING)

USER = 'student'
PASS = 'Meilab123'

def load_config(filename="assignment_interfaces_config.yaml"):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def get_interface_brief_ssh(mgmt_ip, router_name):
    # Define the device connection parameters for Cisco IOS
    device = {
        'device_type': 'cisco_ios',
        'host': mgmt_ip,
        'username': USER,
        'password': PASS,
        'timeout': 10
    }
    
    print(f"\nFetching 'show ip int brief' via SSH for {router_name} ({mgmt_ip})...")
    
    try:
        # Connect directly to the router's CLI
        with ConnectHandler(**device) as net_connect:
            # Run the command and get the exact string output
            output = net_connect.send_command("show ip interface brief | include GigabitEthernet")
            
            print(f"{'Interface':<25} {'IP-Address':<18} {'Status':<12}")
            print("-" * 57)
            
            # Parse the lines to format nicely like our previous scripts
            for line in output.strip().split('\n'):
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 5:
                    name = parts[0]
                    ip = parts[1]
                    # Combine Status and Protocol (e.g., up and up -> up)
                    status = "up" if parts[4] == "up" and parts[5] == "up" else "down"
                    print(f"{name:<25} {ip:<18} {status:<12}")
                    
    except Exception as e:
        print(f"[-] Connection Error on {router_name}: {e}")

def main():
    config_data = load_config()
    for router in config_data.get('routers', []):
        get_interface_brief_ssh(router['mgmt_ip'], router['name'])

if __name__ == "__main__":
    main()
