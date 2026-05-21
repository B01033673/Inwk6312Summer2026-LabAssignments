import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USER = 'student'
PASS = 'Meilab123'

def load_config(filename="assignment_interfaces_config.yaml"):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def configure_interface(mgmt_ip, interface_data):
    # Construct base URL dynamically using the router's management IP
    base_url = f"http://{mgmt_ip}/restconf/api/running/interfaces/interface/"
    url = base_url + interface_data['name']
    
    auth = HTTPBasicAuth(USER, PASS)
    headers = {
        'Accept': 'application/vnd.yang.data+json',
        'Content-Type': 'application/vnd.yang.data+json'
    }
    
    # Construct the JSON payload structure matching standard ietf-interfaces
    payload = {
        "ietf-interfaces:interface": {
            "name": interface_data['name'],
            "description": "Configured via Automation Assignment Script",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": interface_data['ip'],
                        "netmask": interface_data['netmask']
                    }
                ]
            }
        }
    }
    
    try:
        logging.info(f"Sending PUT request to {interface_data['name']} on {mgmt_ip}...")
        response = requests.put(url, auth=auth, headers=headers, data=json.dumps(payload), timeout=10)
        
        # 201 = Created, 204 = No Content (Updated successfully)
        if response.status_code in [200, 201, 204]:
            logging.info(f"SUCCESS: {interface_data['name']} on {mgmt_ip} updated. Status Code: {response.status_code}")
        else:
            logging.error(f"FAILED: {interface_data['name']} on {mgmt_ip}. Status Code: {response.status_code}, Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Connection Exception occurred for {mgmt_ip}: {e}")

def main():
    # Load parameters from the assignment YAML file
    config_data = load_config()
    
    # Loop through each router defined in the YAML file
    for router in config_data.get('routers', []):
        print(f"\n=== Deploying Configuration to {router['name']} ({router['mgmt_ip']}) ===")
        
        # Loop through each target interface on that router
        for interface in router.get('interfaces', []):
            configure_interface(router['mgmt_ip'], interface)

if __name__ == "__main__":
    main()
