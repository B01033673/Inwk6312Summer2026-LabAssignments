import yaml
from netmiko import Netmiko

try:
    hosts = yaml.load(open('host_lab4_exercise.yml'), Loader=yaml.SafeLoader)
except Exception as e:
    print(f"Error accessing inventory file structures: {e}")
    exit(1)

print("\n=== Initiating Lab 4 TextFSM Routing Assessment Execution ===")

for host in hosts["hosts"]:
    try:
        print(f"\nContacting Network Element: {host['name']}...")
        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            port=host["port"],
            device_type=host["type"]
        )
        
        # Interrogate target device and process with TextFSM
        routes = net_connect.send_command("show ip route", use_textfsm=True)
        net_connect.disconnect()
        
        if isinstance(routes, list):
            print(f"--- Parsed Route Tables for {host['name']} ---")
            print(f"{'Protocol':<10} {'Network Prefix':<22} {'Distance':<10} {'Metric':<10}")
            print("-" * 55)
            
            for route in routes:
                proto = route.get('protocol', 'N/A')
                network = route.get('network', 'N/A')
                distance = route.get('distance', 'N/A')
                metric = route.get('metric', 'N/A')
                
                print(f"{proto:<10} {network:<22} {distance:<10} {metric:<10}")
        else:
            print(f"[-] TextFSM layout driver fell back to raw text parsing parsing lines on {host['name']}")
            
    except Exception as e:
        print(f"[-] Execution context terminated unexpectedly on host {host['name']}: {e}")

print("\n=== Dynamic Network Routing Audit Finalized ===")
