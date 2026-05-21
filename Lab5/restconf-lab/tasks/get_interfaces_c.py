import logging
import requests
from requests.auth import HTTPBasicAuth
import json

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

HOST = '192.168.1.107'
USER = 'student'
PASS = 'Meilab123'
BASE_URL = 'http://{0}/restconf/api/running/'.format(HOST)

def get_interfaces(append_url, interface_name, query_params=None):
    # Construct the base URL safely without dangling query strings
    url = BASE_URL + append_url + interface_name
    auth = HTTPBasicAuth(USER, PASS)
    headers = {'Accept': 'application/vnd.yang.data+json'}
    
    logging.info(f"URL ==> {url} | Params ==> {query_params}")
    response = requests.get(url, auth=auth, headers=headers, params=query_params)
    
    if response.status_code == 200:
        logging.info(f"Request was successful on {HOST}, Code: {response.status_code}")
        return json.dumps(response.json(), sort_keys=True, indent=4)
    else:
        logging.error(f"Error encountered during request on {HOST}, Code: {response.status_code}")
        return response.text

# --- Combinations to Experiment With ---

# 1. Test with 'shallow' (returns only top-level properties/keys, useful for a quick summary)
print("--- Testing Shallow ---")
shallow_params = {'shallow': 'true'}
print(get_interfaces("interfaces/interface/", "GigabitEthernet1", query_params=shallow_params))

# 2. Test with 'verbose' (returns full detail including default values if supported by the platform)
print("\n--- Testing Verbose ---")
verbose_params = {'verbose': 'true'}
print(get_interfaces("interfaces/interface/", "GigabitEthernet1", query_params=verbose_params))
