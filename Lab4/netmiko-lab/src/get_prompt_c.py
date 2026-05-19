from netmiko import Netmiko

# Base device template with shared credentials
base_device = {
    "device_type": "cisco_ios",
    "username": "student",
    "password": "Meilab123",
    "secret": "cisco",
    "port": "22",
}

# List of routers in your topology
routers = [
    {"name": "R01", "ip": "192.168.1.101"},
    {"name": "R02", "ip": "192.168.1.102"},
    {"name": "R03", "ip": "192.168.1.103"},
    {"name": "R04", "ip": "192.168.1.104"},
]

# Loop through each router to connect and get prompts
for r in routers:
    print(f"\n--- Connecting to {r['name']} ({r['ip']}) ---")
    
    # Merge the base config with the specific router's IP
    device = base_device.copy()
    device["ip"] = r["ip"]
    
    try:
        net_connect = Netmiko(**device)
        
        print(f"Default prompt: {net_connect.find_prompt()}")
        
        net_connect.send_command_timing("disable")
        print(f"Disable command: {net_connect.find_prompt()}")
        
        net_connect.enable()
        print(f"Enable command: {net_connect.find_prompt()}")
        
        net_connect.disconnect()
        
    except Exception as e:
        print(f"Failed to connect to {r['name']}: {e}")
