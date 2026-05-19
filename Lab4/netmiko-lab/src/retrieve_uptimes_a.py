from netmiko import Netmiko

# List containing all 4 routers in the topology
devices = [
    {"device_type": "cisco_ios", "ip": "192.168.1.101", "username": "student", "password": "Meilab123", "port": "22"},
    {"device_type": "cisco_ios", "ip": "192.168.1.102", "username": "student", "password": "Meilab123", "port": "22"},
    {"device_type": "cisco_ios", "ip": "192.168.1.103", "username": "student", "password": "Meilab123", "port": "22"},
    {"device_type": "cisco_ios", "ip": "192.168.1.104", "username": "student", "password": "Meilab123", "port": "22"}
]

for device in devices:
    try:
        print(f"\nConnecting to {device['ip']}...")
        net_connect = Netmiko(**device)
        
        # Run 'show version' once to gather all needed data
        output = net_connect.send_command("show version")
        net_connect.disconnect()
        
        # Initialize variables
        uptime_info = "Uptime line not found"
        config_register = "Config register not found"
        
        # Loop through the output line by line to extract details dynamically
        for line in output.splitlines():
            if "uptime is" in line:
                # Extracts everything starting from 'uptime is...'
                idx = line.find("uptime is")
                uptime_info = line[idx:]
                
            if "Configuration register is" in line:
                # Grabs the last element of the line (e.g., 0x2102)
                config_register = line.split()[-1]
        
        # Print results for the current device
        print(f"{device['ip']} => {uptime_info}")
        print(f"{device['ip']} => Configuration Register: {config_register}")
        
    except Exception as e:
        print(f"Error connecting to {device['ip']}: {e}")
