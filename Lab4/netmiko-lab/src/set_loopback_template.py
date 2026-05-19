import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# Load the 4 routers and the 4 interfaces from the YAML files
hosts = yaml.load(open('hosts.yml'), Loader=yaml.SafeLoader)
interfaces = yaml.load(open('interfaces.yml'), Loader=yaml.SafeLoader)

# Initialize the Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=True)
template = env.get_template('interfaces_config_template.j2')

# Render the configuration data
loopback_config = template.render(data=interfaces)

# Iterate through each router in the host inventory
for host in hosts["hosts"]:
    try:
        # Connect to the device mapping your specific YAML keys to Netmiko arguments
        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            port=host["port"],
            device_type=host["type"]
        )
        print(f"Logged into {host['name']} successfully")
        
        # Split the rendered multi-line string into a clean list of individual commands
        output = net_connect.send_config_set(loopback_config.split("\n"))
        print(f"Pushed config into {host['name']} successfully")
        
        # Close the connection session cleanly
        net_connect.disconnect()
        
    except Exception as e:
        print(f"Failed to configure host {host['name']}: {e}")

print("Done!")
