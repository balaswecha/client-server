from bottle import route, run, template, HTTPError
from bottle import static_file, request
import json
import os
import sys

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(root_dir)

from modules import bsversionspublisher as vp

with open(os.path.join(root_dir,"config/configuration.json")) as data_file:
    data = json.load(data_file)


@route('/api/versions')
def print_versions():
    return vp.get_versions(data["debs"], data["files"], data["folders"])


@route('/storage')
def server_static():
    file_path = request.query.filepath
    if file_path.startswith(data["fs_root"]):
        return static_file(file_path[len(data["fs_root"]):], root='/opt/balaswecha', download=file_path.split("/")[-1])
    else:
        raise HTTPError(404)

run(host="0.0.0.0", port=8080)
