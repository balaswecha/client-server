import json
import argparse


parser = argparse.ArgumentParser(description='Generate actions-list file')
parser.add_argument('serverfile', metavar='serverFile', type=argparse.FileType('r'), help='Provide server versions file')
parser.add_argument('clientfile', metavar='clientFile', type=argparse.FileType('r'), help='Provide client versions file')
parser.add_argument('-o','--output', default='output.json', type=argparse.FileType('w'), help='Provide Output filename', metavar='OutFile', dest='outFile')
args = parser.parse_args()

with open(args.serverfile.name) as in_file:
    client_data = json.load(in_file)


with open(args.clientfile.name) as in_file:
    server_data = json.load(in_file)


def get_files_to_update(server_files, client_files):
    files_list = []
    for file in server_files:
        if file not in client_files or server_files[file] > client_files[file]:
            files_list.append(file)
    return files_list


def get_files_to_delete(server_files, client_files):
    files_list = []
    for file in client_files:
        if file not in server_files:
            files_list.append(file)
    return files_list


def get_debs_to_install(server_debs, client_debs):
    debs_list = []
    for deb in server_debs:
        if deb not in client_debs or server_debs[deb] != client_debs[deb]:
            debs_list.append(deb)
    return debs_list


def get_debs_to_remove(server_debs, client_debs):
    debs_list = []
    for deb in client_debs:
        if deb not in server_debs:
            debs_list.append(deb)
    return debs_list

server_files = server_data["files"]
client_files = client_data["files"]
server_debs = server_data["debs"]
client_debs = client_data["debs"]


with open(args.outFile.name, "w") as out_file:
    action_map = {"debs_install": get_debs_to_install(server_debs, client_debs),
                  "debs_remove": get_debs_to_remove(server_debs, client_debs),
                  "files_get": get_files_to_update(server_files, client_files),
                  "files_remove": get_files_to_delete(server_files, client_files)
                  }
    json.dump(action_map, out_file)

