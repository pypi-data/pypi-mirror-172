#!/usr/bin/python3

"""Dump all collected info"""

import nb2an.netbox
from rich import print

def main():
    nb = nb2an.netbox.Netbox()
    nb.bootstrap_all_data()
    nb.link_device_data(nb.data["devices"])
    for label in ["devices", "interfaces", "outlets", "power_ports"]:
        print(f"#\n# SECTION: {label}\n#")
        print(nb.data[label])

if __name__ == "__main__":
    main()

