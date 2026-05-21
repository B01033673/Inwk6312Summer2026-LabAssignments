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
    # Querying the native interface configuration root path
    url = f"http://{mgmt_ip}/restconf/api/running/native/interface"
    auth = HTTPBasicAuth(USER, PASS)
    headers = {'Accept': 'application/vnd.yang.data+json'}
    
    print(f"\nFetching interface details for {router_name} ({mgmt_ip})...")
    
    try:
        response = requests.get(url, auth=auth, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get("Cisco-IOS-XE-native:interface", {})
            gig_list = data.get("GigabitEthernet", [])
            
            print(f"{'Interface':<25} {'IP-Address':<18} {'Status':<12}")
            print("-" * 57)
            
            for iface in gig_list:
                # In this data structure, the interface number is stored under 'name' (e.g., "1", "2")
                iface_num = str(iface.get("name", ""))
                full_name = f"GigabitEthernet{iface_num}"
                
                # Dig into Cisco native IP structure
                ip_container = iface.get("ip", {}) or {}
                address_container = ip_container.get("address", {}) or {}
                primary_container = address_container.get("primary", {}) or {}
                
                ip_address = primary_container.get("address", "unassigned")
                
                # Check shutdown status (if 'shutdown' field doesn't exist, it is administratively up)
                shutdown = "shutdown" in iface
                status_str = "down" if shutdown else "up"
                
                print(f"{full_name:<25} {ip_address:<18} {status_str:<12}")
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
