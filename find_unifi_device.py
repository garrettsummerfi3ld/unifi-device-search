import requests
import json

# Load configuration from config.json
try:
  config = json.load(open('config.json'))
except Exception as e:
  print(f"Error occurred while loading config.json: {e}")
  exit(1)

device_mac = ""
device_mac_fuzzy = ""

def process_fuzzy_mac(device_mac_fuzzy):
  '''
  Process a partial MAC address for fuzzy matching, and returning the formatted MAC address substring.
  '''
  lowered_fuzzy = device_mac_fuzzy.lower()

  # Validate fuzzy MAC address format
  if len(lowered_fuzzy) % 2 != 0:
    print("Fuzzy MAC address must have an even number of characters.")
    return None
  segmented = [lowered_fuzzy[i:i+2] for i in range(0, len(lowered_fuzzy), 2)]
  return ':'.join(segmented)

def find_device():
  '''
  Find a device by its MAC address via REST API.
  '''
  
  # Local variables
  found_device = False
  fuzzy_mac = process_fuzzy_mac(device_mac_fuzzy)

  # Iterate through each controller
  for controller in config.get("controllers", []):
    api_key = controller.get("api_key")
    base_url = controller.get("address")

    payload = {}
    headers = {
      'Accept': 'application/json',
      'X-API-KEY': api_key
    }
    try:
      print(f'Searching site {site.get("name")}')
      # Get list of sites from controller and parse into JSON
      list_sites = requests.request("GET", base_url + "proxy/network/integration/v1/sites", headers=headers, data=payload, verify=False)
      sites = list_sites.json().get('data', [])

      # Iterate through each site and get its devices in JSON format
      for site in sites:
        list_devices = requests.request("GET", base_url + f"proxy/network/integration/v1/sites/{site.get('id')}/devices", headers=headers, data=payload, verify=False)
        devices = list_devices.json().get('data', [])
        for device in devices:
          # Check for exact MAC address match
          if device.get("macAddress") == device_mac:
            found_device = True
            print("Found device with matching MAC address.")
            print(f"Site ID: {site.get('id')}\nSite Name: {site.get('name')}")
            print(f'Device ID: {device.get("id")}\nName: {device.get("name")}\nModel: {device.get("model")}\nMAC: {device.get("macAddress")}')
          # Check for fuzzy/substring MAC address match
          elif device.get("macAddress").find(fuzzy_mac) != -1:
            found_device = True
            print("Found device with fuzzy matching MAC address.")
            print(f"Site ID: {site.get('id')}\nSite Name: {site.get('name')}")
            print(f'Device ID: {device.get("id")}\nName: {device.get("name")}\nModel: {device.get("model")}\nMAC: {device.get("macAddress")}')
      # End of site/device iteration
      if not found_device:
        print(f"Device with MAC address {device_mac} or {device_mac_fuzzy} not found.")
    except Exception as e:
      print(f"Error occurred while searching for device: {e}")

if __name__ == "__main__":
  find_device()