import subprocess

def get_route(subnet):
    route = subprocess.run(['ip', 'route', 'get', subnet], capture_output=True, text=True)
    if route.returncode == 0:
        return route.stdout.strip().split()[4]
    else:
        gateway = route.stderr.strip().split()[-1]
        return get_route(gateway)

subnet = input("Enter the subnet to look up: ")
forwarding_interface = get_route(subnet)
print("Forwarding interface:", forwarding_interface)
