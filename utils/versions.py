#!/usr/bin/env python3
import argparse
import json
import os
import bsversionspublisher as vp

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


parser = argparse.ArgumentParser(description='Generate BalaSwecha version file')
parser.add_argument('-o','--output', default='output.json', type=argparse.FileType('w'), help='Provide Output filename to write versions data into', metavar='OutFile', dest='outFile')
args = parser.parse_args()

with open(os.path.join(root_dir,"config/configuration.json")) as data_file:
    data = json.load(data_file)

with open(args.outFile.name,"w") as out_file:
    data = vp.get_versions(data)
    json.dump(data, out_file)