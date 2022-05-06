import subprocess
import requests

wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
data = wifi.decode('utf-8')
if "VIT2.4G" in data:
    print("Connected to VIT2.4G")
elif "VIT5G" in data:
    print("Connected to VIT5G")
else:
    print("Not connected to VIT wifi")

