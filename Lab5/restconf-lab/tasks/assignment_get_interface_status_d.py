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
    # The actual operational tracking data path for IOS-XE 16.5
    url = f"http://{mgmt_ip}/restconf/api/operational/interfaces-oper"
    auth = HTTPBasicAuth(USER, PASS)
    headers = {'Accept': 'application/vnd.yang.data+json'}
    
    print(f"\nFetching interface details for {router_name} ({mgmt_ip})...")
    
    try:
        response = requests.get(url, auth=auth, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Extract from Cisco native operational model
            oper_container = data.get("Cisco-IOS-XE-interfaces-oper:interfaces-oper", {})
            interfaces = oper_container.get("interface-info", [])
            
            print(f"{'Interface':<25} {'IP-Address':<18} {'Status':<12}")
            print("-" * 57)
            
            for iface in interfaces:
                name = iface.get("name", "Unknown")
                ip_address = iface.get("description", "unassigned") # Fallback key init
                
                # Extract the active operational IP address
                ip_address = iface.get("ipv4", "unassigned")
                if not ip_address or ip_address == "0.0.0.0":
                    ip_address = "unassigned"
                    
                # Extract status (up/down matching 'sh ip int br')
                status = iface.get("status", "down")
                if status == "IF_OPER_UP":
                    status_str = "up"
                elif status == "IF_OPER_DOWN":
                    status_str = "down"
                else:
                    status_str = status.replace("IF_OPER_", "").lower()
                
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
