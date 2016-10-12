#!/usr/bin/env python3
import argparse
import json
import os
import balaswecha_sync as bsync

root_dir = "/usr/lib/balaswecha/balaswecha-sync"


parser = argparse.ArgumentParser(description='Generate BalaSwecha version file')
parser.add_argument('-o','--output', default='output.json', type=argparse.FileType('w'), help='Provide Output filename to write versions data into', metavar='OutFile', dest='outFile')
args = parser.parse_args()

with open(os.path.join(root_dir,"config/configuration.json")) as data_file:
    conf_data = json.load(data_file)

with open(args.outFile.name,"w") as out_file:
    data = bsync.get_versions(conf_data["debs"], conf_data["files"], conf_data["folders"])
    json.dump(data, out_file)