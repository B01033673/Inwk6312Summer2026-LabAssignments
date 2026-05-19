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
        print(f"\n========================================================================")
        print(f" Routing Table Data for Router: {device['ip']} ")
        print(f"========================================================================")
        print(f"{'Protocol':<10} {'Network':<20} {'Distance':<10} {'Metric':<10}")
        print("-" * 55)
        
        net_connect = Netmiko(**device)
        
        # Pulling structured routing output using TextFSM
        routes = net_connect.send_command("show ip route", use_textfsm=True)
        net_connect.disconnect()
        
        # Verify TextFSM successfully returned a list of route dictionaries
        if isinstance(routes, list):
            for route in routes:
                # Safely get values using the exact TextFSM keys (with defaults if empty)
                proto = route.get('protocol', 'N/A')
                net = route.get('network', 'N/A')
                dist = route.get('distance', 'N/A')
                met = route.get('metric', 'N/A')
                
                # Format into a clean table structure
                print(f"{proto:<10} {net:<20} {dist:<10} {met:<10}")
        else:
            print("Could not parse 'show ip route' output with TextFSM.")
            
    except Exception as e:
        print(f"Error connecting to {device['ip']}: {e}")
