import json
import os
import bsversionspublisher as vp

conf_file = "config/configuration.json"
root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

with open(os.path.join(root_dir, conf_file)) as config_file:
    config = json.load(config_file)

server_data = vp.get_server_json(config["server_versions_api"])
client_data = vp.get_versions(config["debs"], config["files"], config["folders"])
operations = vp.get_upgrade_operations(server_data["files"], server_data["debs"], client_data["files"],client_data["debs"])
vp.run_upgrade_operations(config["server_root"], operations)

server_conf = vp.get_server_json(config["server_conf_api"])

with open(os.path.join(root_dir, conf_file),"w") as config_file:
    data = {"server_version_api": config["server_versions_api"],
            "server_conf_api": config["server_conf_api"],
            "server_root": config["server_root"],
            "fs_root": server_conf["fs_root"],
            "folders": server_conf["folders"],
            "files": server_conf["files"],
            "debs": server_conf["debs"]
            }
    json.dump(data, config_file)


