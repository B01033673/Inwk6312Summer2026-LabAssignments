from netmiko import Netmiko

# Defining each device separately
r1 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.101",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

r2 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.102",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

r3 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.103",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

r4 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.104",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

# Loop through all defined routers in the topology
for device in (r1, r2, r3, r4):
    try:
        print(f"\n=========================================")
        print(f" Interfaces on Router: {device['ip']} ")
        print(f"=========================================")
        
        net_connect = Netmiko(**device)
        
        # Pulling structured output using TextFSM
        output = net_connect.send_command("show ip interface brief", use_textfsm=True)
        net_connect.disconnect()
        
        # Verify TextFSM returned a valid list of dictionaries
        if isinstance(output, list):
            for interface in output:
                # Using the correct key 'interface'
                print(f" - {interface['interface']}")
        else:
            print("Could not parse output with TextFSM.")
            
    except Exception as e:
        print(f"Error connecting to {device['ip']}: {e}")
