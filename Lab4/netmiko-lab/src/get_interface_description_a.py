from netmiko import ConnectHandler

# Defining each device separately as per the example style
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

# The list of commands we want to execute on every router
commands = [
    "show ip interface brief",
    "show ip route",
    "show running-config | section ospf"
]

# Looping through all defined routers in the topology
for device in (r1, r2, r3, r4):
    try:
        print(f"\n========================================================================")
        print(f"=== CONNECTING TO ROUTER: {device['ip']} ===")
        print(f"========================================================================")
        
        net_connect = ConnectHandler(**device)
        
        # Loop through each command in our list
        for cmd in commands:
            print(f"\n--- [Executing: {cmd}] ---")
            output = net_connect.send_command(cmd)
            print("-" * 100)
            print(output if output.strip() else " (No output returned or protocol not configured) ")
            print("-" * 100)
            
        net_connect.disconnect()
        
    except Exception as e:
        print(f"Could not connect to {device['ip']}: {e}")
