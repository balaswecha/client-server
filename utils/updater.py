import json
import sys
import os

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(root_dir)

from modules import bsversionspublisher as vp


with open(os.path.join(root_dir, "config/configuration.json")) as config_file:
    config = json.load(config_file)

server_data = vp.get_server_versions(config["server_versions_api"])
client_data = vp.get_versions(config["debs"], config["files"], config["folders"])
operations = vp.get_upgrade_operations(server_data["files"], server_data["debs"], client_data["files"],client_data["debs"])
vp.run_upgrade_operations(config["server_root"], operations)


