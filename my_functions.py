import yaml
from netmiko import Netmiko
from flask import jsonify 

with open("inventory.yaml") as f:
    data = yaml.safe_load(f)


def get_int(ip):
    for v in data["Devices"].values():
        if v["host"] == ip:
            connect = Netmiko(**v)
            output = connect.send_command("show ip interface brief", use_genie=True)
            return jsonify(output)
        else:
            pass 


def conf_vlan(ip , vlan):
    for v in data["Devices"].values():
        if v["host"] == ip:
            connect = Netmiko(**v)
            connect.send_config_set(f"vlan {vlan}")
            output = connect.send_command(f"show vlan" , use_genie=True)

            return jsonify(output)