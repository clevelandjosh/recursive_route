import re
import subprocess

def get_route(subnet):
    route = subprocess.run(['cli', '-c', f"show route {subnet} detail"], capture_output=True, text=True)
    match = re.search(r'Next hop: (\S+)', route.stdout)
    if match:
        return match.group(1)
    else:
        match = re.search(r'via (\S+),', route.stdout)
        if match:
            return get_route(match.group(1))
        else:
            raise Exception("Route not found")

subnet = input("Enter the subnet to look up: ")
forwarding_interface = get_route(subnet)
print("Forwarding interface:", forwarding_interface)
