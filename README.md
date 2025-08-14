# Unifi Device Search

> [!NOTE]
> This is a work in progress and the functionality and usability may change.
>
> Documentation is limited and may not cover all use cases.
>
> Please provide feedback or contribute to the project to help improve it.

## Prerequisites

- Python 3.6 or later
- `requests`

## How to use

Create a `config.json` file in the root of the folder.

```json
{
  "controllers": [
    {
      "name": "Unifi Site Generic",
      "address": "https://unifi.example/",
      "api_key": "PLEASE-PUT-API-KEY-HERE-AND-KEEP-IT-SECRET"
    }
  ]
}
```

In the `find_unifi_device.py`, you have two options to search for devices. "Fuzzy" MAC or the full MAC address.

Fuzzy MACs are partial MAC addresses that can match multiple devices. For example, if you have a device with the MAC address `00:11:22:33:44:55`, you can use the fuzzy MAC `001122` to find it.

Full MAC addresses are the complete 12-digit hexadecimal representation of a MAC address. For example, `00:11:22:33:44:55` is a full MAC address.

There are two variables you can change:

```py
device_mac = ""
device_mac_fuzzy = ""
```

Replace them with the MAC addresses you want to search for. For example:

```py
device_mac = "00:11:22:33:44:55"
device_mac_fuzzy = "001122"
```

Once replaced, run `find_unifi_device.py` to search for the device.
