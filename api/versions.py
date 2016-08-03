from bottle import route, run, template
import json
import os
import sys

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(root_dir)

from modules import versionspublisher as vp

@route('/api/versions')
def print_versions():

    with open(os.path.join(root_dir,"config/configuration.json")) as data_file:
        data = json.load(data_file)

    return {"debs": vp.debs_version(data["debs"]), "files": vp.files_version(data["files"], data["folders"])}

run(host="localhost", port=8080)
