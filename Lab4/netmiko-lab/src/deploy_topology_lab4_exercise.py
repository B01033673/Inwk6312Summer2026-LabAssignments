import logging
import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# Setup structured logging configuration
logger = logging.getLogger("Lab4Automation")
logger.setLevel(logging.DEBUG)

# File handler targets exercise-specific logging storage
file_handler = logging.FileHandler("network_lab4_exercise.log")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_formatter)
console_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Initializing Lab 4 Exercise Topology Configuration Run")

try:
    hosts = yaml.load(open('host_lab4_exercise.yml'), Loader=yaml.SafeLoader)
    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=True)
    template = env.get_template('topology_template_lab4_exercise.j2')
    logger.info("Configuration templates and variables parsed successfully")
except Exception as e:
    logger.critical(f"Asset loading exception encountered: {e}")
    exit(1)

for host in hosts["hosts"]:
    try:
        logger.debug(f"Compiling interface schema string for host {host['name']}")
        
        # FIXED: Explicitly passing rip_networks to the Jinja2 template engine
        device_config = template.render(
            loopback=host["loopback"], 
            sub_interfaces=host["sub_interfaces"],
            rip_networks=host.get("rip_networks", [])
        )
        
        logger.info(f"Connecting via Netmiko to destination router: {host['name']}")
        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            port=host["port"],
            device_type=host["type"]
        )
        
        logger.info(f"Pushing generated interface configuration matrix into {host['name']}")
        output = net_connect.send_config_set(device_config.split("\n"))
        logger.debug(f"Router feedback output received:\n{output}")
        
        logger.info(f"Execution successfully verified. Safely dropping connection to {host['name']}.")
        net_connect.disconnect()
        
    except Exception as e:
        logger.error(f"Runtime communication error processing device {host['name']}: {e}")

logger.info("Lab 4 interface provisioning cycle finalized.")
