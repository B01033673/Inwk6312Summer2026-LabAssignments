from netmiko import ConnectHandler

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

for device in (r1, r2, r3, r4):
    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command("show interface description")
        net_connect.disconnect()
        print("-" * 100)
        print(f"Device IP: {device['ip']}")
        print(output)
        print("-" * 100)
    except Exception as e:
        print("-" * 100)
        print(f"Failed to connect to {device['ip']}: {e}")
        print("-" * 100)
