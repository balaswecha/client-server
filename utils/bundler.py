#!/usr/bin/env python3
import argparse
import json
import os
import balaswecha_sync as bsync

parser = argparse.ArgumentParser(description='Generate BalaSwecha update bundle file')
parser.add_argument('versionfile', metavar='versionFile', type=argparse.FileType('r'), help='Provide versions file')
parser.add_argument('-b','--bundle', default='update-bundle.zip', type=argparse.FileType('w'), help='Bundle filename', metavar='BundleFile', dest='bundleFile')
args = parser.parse_args()

conf_file = "config/configuration.json"
root_dir = "/usr/lib/balaswecha/balaswecha-sync"

with open(os.path.join(root_dir, conf_file)) as config_file:
    server_config = json.load(config_file)


with open(args.versionfile.name) as version_file:
    client_data = json.load(version_file)

server_data = bsync.get_versions(server_config["debs"], server_config["files"], server_config["folders"])
operations = bsync.get_upgrade_operations(server_data["files"], server_data["debs"], client_data["files"],client_data["debs"])
bsync.gen_upgrade_bundle(args.bundleFile.name, operations, server_config)

