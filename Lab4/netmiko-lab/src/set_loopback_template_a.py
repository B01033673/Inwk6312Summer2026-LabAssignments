import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# Load the updated host file mapping
hosts = yaml.load(open('hosts_a.yml'), Loader=yaml.SafeLoader)

env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=True)
template = env.get_template('interfaces_config_template_a.j2')

for host in hosts["hosts"]:
    try:
        # Render uniquely for this host's loopback block
        loopback_config = template.render(loopback=host["loopback"])
        
        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            port=host["port"],
            device_type=host["type"]
        )
        print(f"Logged into {host['name']} successfully")
        
        # Split multi-line configuration blocks cleanly for Netmiko
        output = net_connect.send_config_set(loopback_config.split("\n"))
        print(f"Pushed specific loopback into {host['name']} successfully")
        net_connect.disconnect()
        
    except Exception as e:
        print(f"Error on {host['name']}: {e}")

print("Done!")
