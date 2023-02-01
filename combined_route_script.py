import re
import subprocess
import platform

def get_linux_route(subnet):
    route = subprocess.run(['ip', 'route', 'get', subnet], capture_output=True, text=True)
    if route.returncode == 0:
        return route.stdout.strip().split()[4]
    else:
        gateway = route.stderr.strip().split()[-1]
        return get_linux_route(gateway)

def get_juniper_route(subnet):
    route = subprocess.run(['cli', '-c', f"show route {subnet} detail"], capture_output=True, text=True)
    match = re.search(r'Next hop: (\S+)', route.stdout)
    if match:
        return match.group(1)
    else:
        match = re.search(r'via (\S+),', route.stdout)
        if match:
            return get_juniper_route(match.group(1))
        else:
            raise Exception("Route not found")

subnet = input("Enter the subnet to look up: ")

platform_name = platform.system().lower()
if platform_name == 'linux':
    forwarding_interface = get_linux_route(subnet)
elif platform_name == 'juniper':
    forwarding_interface = get_juniper_route(subnet)
else:
    raise Exception(f"Unsupported platform: {platform_name}")

print("Forwarding interface:", forwarding_interface)
