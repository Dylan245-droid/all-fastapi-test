import subprocess

# using the check_output() for having the network term retrieval
devices = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])

# decode it to strings
devices = devices.decode('ascii')

s = devices.replace("\r", "")

# displaying the information
nearby = [x[x.find(':') + 1:].replace('\r', '').strip() for x in devices.split('\n') if "SSID" in x]