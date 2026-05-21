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
    url = f"http://{mgmt_ip}/restconf/api/running/interfaces"
    auth = HTTPBasicAuth(USER, PASS)
    headers = {'Accept': 'application/vnd.yang.data+json'}
    
    print(f"\nFetching interface details for {router_name} ({mgmt_ip})...")
    
    try:
        response = requests.get(url, auth=auth, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            interfaces = data.get("ietf-interfaces:interfaces", {}).get("interface", [])
            
            print(f"{'Interface':<25} {'IP-Address':<18} {'Enabled':<12}")
            print("-" * 57)
            
            for iface in interfaces:
                name = iface.get("name", "Unknown")
                enabled = iface.get("enabled", True)
                status_str = "up" if enabled else "down"
                
                ip_address = "unassigned"
                
                # Method 1: Try Standard ietf-ip pathway
                ipv4_data = iface.get("ietf-ip:ipv4", {}) or {}
                addresses = ipv4_data.get("address", [])
                if addresses:
                    ip_address = addresses[0].get("ip", "unassigned")
                
                # Method 2: Fallback to Cisco-IOS-XE-native structural format if still unassigned
                if ip_address == "unassigned":
                    cisco_ipv4 = iface.get("Cisco-IOS-XE-native:ipv4", {}) or {}
                    cisco_addresses = cisco_ipv4.get("address", {}) or {}
                    primary_address = cisco_addresses.get("primary", {}) or {}
                    if primary_address:
                        ip_address = primary_address.get("address", "unassigned")
                
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
