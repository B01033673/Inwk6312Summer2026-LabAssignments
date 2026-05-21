import logging
import requests
from requests.auth import HTTPBasicAuth
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

USER = 'student'
PASS = 'Meilab123'

def load_config(filename="assignment_interfaces_config.yaml"):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def get_interface_brief(mgmt_ip, router_name):
    # Swapped out to use the verified /api/running/ root path
    url = f"http://{mgmt_ip}/restconf/api/running/interfaces"
    auth = HTTPBasicAuth(USER, PASS)
    headers = {'Accept': 'application/vnd.yang.data+json'}
    
    print(f"\nFetching interface details for {router_name} ({mgmt_ip})...")
    
    try:
        response = requests.get(url, auth=auth, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Handle native structure variations
            interfaces = data.get("ietf-interfaces:interfaces", {}).get("interface", [])
            
            print(f"{'Interface':<25} {'IP-Address':<18} {'Enabled':<12}")
            print("-" * 57)
            
            for iface in interfaces:
                name = iface.get("name", "Unknown")
                enabled = iface.get("enabled", True)
                
                # Dig down into the list to extract the configured IPv4 address
                ipv4_data = iface.get("ietf-ip:ipv4", {}).get("address", [])
                ip_address = ipv4_data[0].get("ip", "unassigned") if ipv4_data else "unassigned"
                
                status_str = "up" if enabled else "down"
                
                print(f"{name:<25} {ip_address:<18} {status_str:<12}")
        else:
            print(f"[-] Failed to fetch data from {router_name}. HTTP Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] Connection Error on {router_name}: {e}")

def main():
    config_data = load_config()
    for router in config_data.get('routers', []):
        get_interface_brief(router['mgmt_ip'], router['name'])

if __name__ == "__main__":
    main()
