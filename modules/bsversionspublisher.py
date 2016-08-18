from subprocess import Popen, PIPE
from functools import partial
import os
import requests


def get_server_versions(server_api):
    resp = requests.get(server_api)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {}


def get_versions(config_debs, config_files, config_folders):
    return {"debs": __debs_version(config_debs), "files": __files_version(config_files, config_folders)}


def get_upgrade_operations(server_files, server_debs, client_files, client_debs):

    return {"debs_install": __get_debs_to_install(server_debs, client_debs),
            "debs_remove": __get_debs_to_remove(server_debs, client_debs),
            "files_get": __get_files_to_update(server_files, client_files),
            "files_remove": __get_files_to_delete(server_files, client_files)
            }


def run_upgrade_operations(server_root, operations):
    __update_files(server_root, operations["files_get"])
    __delete_files(operations["files_remove"])
    __remove_debs(operations["debs_remove"])
    __install_debs(operations["debs_install"])


def __delete_files(files):
    for file in files:
        os.remove(file)


def __update_files(server_root, files):
    for file in files:
        if not os.path.isdir(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        with open(file,'wb') as handle:
            response = requests.get(server_root + "?filepath=" + file, stream=True)
            if not response.ok:
                print("couldn't get the file:"+file)
            else:
                for chunk in response.iter_content(1024):
                    handle.write(chunk)


def __install_debs(debs):
    process_open = Popen(["apt-get", "install", "-y", "-s"] + debs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process_open.communicate()[0]
    return process_open.returncode


def __remove_debs(debs):
    process_open = Popen(["apt-get", "remove", "-y", "-s"] + debs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process_open.communicate()[0]
    return process_open.returncode


def __debs_version(included_debs):
    debs_list = __get_installed_debs_list(included_debs)
    return __collate_list_of_maps(debs_list)


def __files_version(file_list, dir_list):
    files_map = {}
    for folder in dir_list:
        __walk_and_update_map(folder, files_map)
    for file in file_list:
        __update_files_map(file, files_map)
    return files_map


def __map_package(package_with_version):
    package, version = package_with_version.split()
    return {package: version}


def __exclude_package(package_with_version, included_debs):
    package, version = package_with_version.split()
    return package in included_debs


def __get_installed_debs_list(included_debs):
    process_open = Popen(["dpkg-query", "-W", "--showformat=${Package} ${Version}\n"], \
                         stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    process_stdout = process_open.communicate()[0]
    pkg_list = process_stdout.strip().split("\n")
    return list(map(__map_package, filter(partial(__exclude_package, included_debs=included_debs), pkg_list)))


def __collate_list_of_maps(debs_list):
    return {p: v for d in debs_list for p, v in d.items()}


def __gen_timestamp(filename):
    modified_time = str(os.stat(filename).st_mtime).split(".")[0]
    return modified_time


def __update_files_map(filename, files_map):
    files_map[filename] = __gen_timestamp(filename)


def __walk_and_update_map(folder, files_map):
    for root, folders, files in os.walk(folder):
        for file in files:
            filename = os.path.join(root, file)
            __update_files_map(filename, files_map)


def __get_files_to_update(server_files, client_files):
    files_list = []
    for file in server_files:
        if file not in client_files or server_files[file] > client_files[file]:
            files_list.append(file)
    return files_list


def __get_files_to_delete(server_files, client_files):
    files_list = []
    for file in client_files:
        if file not in server_files:
            files_list.append(file)
    return files_list


def __get_debs_to_install(server_debs, client_debs):
    debs_list = []
    for deb in server_debs:
        if deb not in client_debs or server_debs[deb] != client_debs[deb]:
            debs_list.append(deb)
    return debs_list


def __get_debs_to_remove(server_debs, client_debs):
    debs_list = []
    for deb in client_debs:
        if deb not in server_debs:
            debs_list.append(deb)
    return debs_list
