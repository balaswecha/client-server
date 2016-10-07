#!/usr/bin/env python3
import argparse
import json
import os
import bsversionspublisher as vp

parser = argparse.ArgumentParser(description='Generate BalaSwecha update bundle file')
parser.add_argument('versionfile', metavar='versionFile', type=argparse.FileType('r'), help='Provide versions file')
parser.add_argument('-b','--bundle', default='update-bundle.zip', type=argparse.FileType('w'), help='Bundle filename', metavar='BundleFile', dest='bundleFile')
args = parser.parse_args()

conf_file = "config/configuration.json"
root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

with open(os.path.join(root_dir, conf_file)) as config_file:
    server_config = json.load(config_file)


with open(args.versionfile.name) as version_file:
    client_data = json.load(version_file)

server_data = vp.get_versions(server_config["debs"], server_config["files"], server_config["folders"])
operations = vp.get_upgrade_operations(server_data["files"], server_data["debs"], client_data["files"],client_data["debs"])
vp.gen_upgrade_bundle(args.bundleFile.name, operations, server_config)

