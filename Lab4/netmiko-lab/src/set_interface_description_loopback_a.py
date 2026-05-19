from netmiko import Netmiko

# List of all routers, keeping tracking information organized
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.101",
        "username": "student",
        "password": "Meilab123",
        "port": "22",
        "loopback_ip": "1.1.1.1"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.102",
        "username": "student",
        "password": "Meilab123",
        "port": "22",
        "loopback_ip": "2.2.2.2"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.103",
        "username": "student",
        "password": "Meilab123",
        "port": "22",
        "loopback_ip": "3.3.3.3"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.104",
        "username": "student",
        "password": "Meilab123",
        "port": "22",
        "loopback_ip": "4.4.4.4"
    }
]

for device in devices:
    try:
        print(f"\n==================================================")
        print(f" Configuring Loopback0 on Router: {device['ip']} ")
        print(f"==================================================")
        
        # 1. Create a clean copy of the connection settings
        connection_params = device.copy()
        
        # 2. Extract and remove the custom key so Netmiko doesn't see it
        target_loopback = connection_params.pop("loopback_ip")
        
        # 3. Build the config set using our isolated variable
        loopback_config = [
            "interface Loopback0",
            f"ip address {target_loopback} 255.255.255.255",
            "description Loopback configured via Netmiko script"
        ]
        
        # Connect using only the parameters Netmiko expects
        net_connect = Netmiko(**connection_params)
        
        # Send configurations
        output = net_connect.send_config_set(loopback_config)
        print(output)
        
        net_connect.disconnect()
        
    except Exception as e:
        print(f"Error configuring device {device['ip']}: {e}")
