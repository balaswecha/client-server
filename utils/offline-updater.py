#!/usr/bin/env python3
import argparse
import json
import os
import balaswecha_sync as bsync

parser = argparse.ArgumentParser(description='Update BalaSwecha from bundle file')
parser.add_argument('-b','--bundle', default='update-bundle.zip', type=argparse.FileType('r'), help='Bundle filename', metavar='BundleFile', dest='bundleFile')
args = parser.parse_args()

conf_file = "config/configuration.json"
root_dir = "/usr/lib/balaswecha/balaswecha-sync"

with open(os.path.join(root_dir, conf_file)) as config_file:
    client_config = json.load(config_file)

bsync.upgrade_from_bundle(args.bundleFile.name)
server_conf = bsync.get_server_json_from_bundle(args.bundleFile.name)

with open(os.path.join(root_dir, conf_file),"w") as config_file:
    data = {"server_versions_api": client_config["server_versions_api"],
            "server_conf_api": client_config["server_conf_api"],
            "server_root": client_config["server_root"],
            "fs_root": server_conf["fs_root"],
            "folders": server_conf["folders"],
            "files": server_conf["files"],
            "debs": server_conf["debs"]
            }
    json.dump(data, config_file)

